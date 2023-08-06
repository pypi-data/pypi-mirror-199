from collections import defaultdict
from functools import lru_cache
from typing import Type, Any, Optional, TypeVar, Sequence

from tortoise.fields import ManyToManyRelation
from tortoise.models import MetaInfo
from tortoise.queryset import QuerySet
from tortoise.transactions import in_transaction
from fastapi import BackgroundTasks, Request

from ex_fastapi import CamelModel
from ex_fastapi.routers.base_crud_service import BaseCRUDService, ModelPrefix, PK, \
    Handler, QsRelatedFunc, QsAnnotateFunc, QsDefaultFiltersFunc, FKGetInstance
from ex_fastapi.routers.exceptions import \
    ItemNotFound, \
    NotUnique, NotFoundFK, FieldRequired, \
    ListFieldError, ObjectErrors
from ex_fastapi.routers.filters import BaseFilter
from . import BaseModel


TORTOISE_MODEL = TypeVar('TORTOISE_MODEL', bound=BaseModel)


class TortoiseCRUDService(BaseCRUDService[PK, TORTOISE_MODEL]):
    model: Type[TORTOISE_MODEL]
    opts: MetaInfo

    def __init__(
            self,
            db_model: Type[TORTOISE_MODEL],
            *,
            read_schema: Type[CamelModel] = None,
            read_many_schema: Type[CamelModel] = None,
            read_list_item_schema: Type[CamelModel] = None,
            create_schema: Type[CamelModel] = None,
            edit_schema: Type[CamelModel] = None,
            queryset_select_related: QsRelatedFunc | set[str] = None,
            queryset_prefetch_related: QsRelatedFunc | set[str] = None,
            queryset_annotate_fields: QsAnnotateFunc | dict[str, Any] = None,
            queryset_default_filters: QsDefaultFiltersFunc | dict[str, Any] = None,
            node_key: str = 'parent_id',
            create_handlers: dict[str, Handler] = None,
            edit_handlers: dict[str, Handler] = None,
            fk_get_instance_map: dict[str, FKGetInstance[PK, TORTOISE_MODEL]] = None,
            defaults: dict[str, dict[str, Any]] = None,
    ):
        super().__init__(db_model)  # чтобы не ругался
        self.model = db_model
        self.opts = self.model._meta
        self.pk_field_type = self.opts.pk.field_type  # type: ignore
        self.pk_attr = self.opts.pk_attr

        self.read_schema = read_schema
        self.list_item_schema = read_list_item_schema or self.read_schema
        self.read_many_schema = read_many_schema or self.list_item_schema
        self.create_schema = create_schema
        self.edit_schema = edit_schema

        self.queryset_select_related = get_qs_build_func(
            'queryset_select_related', self.model, queryset_select_related
        )
        self.queryset_prefetch_related = get_qs_build_func(
            'queryset_prefetch_related', self.model, queryset_prefetch_related
        )
        self.queryset_annotate_fields = get_qs_build_func(
            'queryset_annotate_fields', self.model, queryset_annotate_fields
        )
        self.queryset_default_filters = get_qs_build_func(
            'queryset_default_filters', self.model, queryset_default_filters
        )
        self.fk_get_instance_map = fk_get_instance_map or {}
        self.defaults = defaults or {}

        self.node_key = node_key

        self.create_handlers = create_handlers or {}
        self.edit_handlers = edit_handlers or {}

    def get_queryset(
            self,
            request: Optional[Request] = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> QuerySet[TORTOISE_MODEL]:
        if request is None:
            path, method = '', ''
        else:
            path, method = request.scope['route'].path, request.method

        query = self.model.all()
        if default_filters := self.queryset_default_filters(path, method):
            query = query.filter(**default_filters)
        if annotate_fields := self.queryset_annotate_fields(path, method):
            query = query.annotate(**annotate_fields)
        if final_select_related := {*self.queryset_select_related(path, method), *select_related}:
            query = query.select_related(*final_select_related)
        if final_prefetch_related := {*self.queryset_prefetch_related(path, method), *prefetch_related}:
            query = query.prefetch_related(*final_prefetch_related)
        return query

    async def get_all(
            self,
            skip: Optional[int], limit: Optional[int],
            sort: set[str],
            filters: list[BaseFilter],
            *,
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> tuple[list[TORTOISE_MODEL], int]:
        query = self.get_queryset(request=request, select_related=select_related, prefetch_related=prefetch_related)
        for f in filters:
            query = f.filter(query)
        base_query = query
        if sort:
            query = query.order_by(*sort)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        async with in_transaction():
            result = await query
            count = await base_query.count()
        return result, count

    def _get_many_queryset(
            self,
            item_ids: list[PK],
            *,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> QuerySet[TORTOISE_MODEL]:
        return self.get_queryset(
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related
        ).filter(pk__in=item_ids)

    async def get_many(
            self,
            item_ids: list[PK],
            *,
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> list[TORTOISE_MODEL]:
        return await self._get_many_queryset(
            item_ids,
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related
        )

    async def get_one(
            self,
            item_id: PK,
            *,
            field_name: str = 'pk',
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> Optional[TORTOISE_MODEL]:
        instance = await self.get_queryset(
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related,
        ).get_or_none(**{field_name: item_id})
        if instance is None:
            raise ItemNotFound()
        return instance

    async def get_tree_node(
            self,
            node_id: Optional[PK],
            *,
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> list[TORTOISE_MODEL]:
        return await self.get_queryset(
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related,
        ).filter(**{self.node_key: node_id})

    async def create(
            self,
            data: CamelModel,
            *,
            exclude: set[str] = None,
            model: Type[TORTOISE_MODEL] = None,
            background_tasks: BackgroundTasks = None,
            defaults: dict[str, Any] = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> TORTOISE_MODEL:
        model: Type[TORTOISE_MODEL] = model or self.model
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_new_instance():
            not_unique = await model.check_unique(data.dict(include=model._meta.db_fields))
            for field_name in not_unique:
                errors.add(field_name, NotUnique)

            # Сначала создаём o2o и fk, потому что они могут быть not null, из-за этого вылетает ошибка.
            created_o2o, picked_fks = {}, {}

            for o2o_field_name in o2o_fields:
                try:
                    o2o_instance = await self.create_o2o(model, o2o_field_name, data, exclude_dict, prefix=prefix)
                    created_o2o[o2o_field_name] = o2o_instance
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model, fk_fields, data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors
            try:
                instance: TORTOISE_MODEL = await self.handle_create(model, prefix=prefix)(
                    data, should_exclude={*exclude_dict['__root__'], *fk_fields},
                    defaults={**self.defaults.get(prefix, {}), **defaults, **created_o2o, **picked_fks}
                )
            except ObjectErrors as e:
                raise errors.merge(e)

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.create_backward_o2o(instance, bo2o_field_name, data, exclude_dict, prefix=prefix)
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_field_name in bfk_fields:
                try:
                    await self.create_backward_fk(instance, bfk_field_name, data, exclude_dict, prefix=prefix)
                except ListFieldError as e:
                    errors.add(bfk_field_name, e)

            for m2m_field_name in m2m_fields:
                await self.save_m2m(instance, data, m2m_field_name, prefix=prefix, clear=False)

            if errors:
                raise errors
            return instance

        if inside_transaction:
            return await get_new_instance()
        else:
            async with in_transaction():
                new_instance = await get_new_instance()
            return await self.get_one(
                new_instance.pk,
                request=request,
                select_related=select_related,
                prefetch_related=prefetch_related,
            )

    async def create_o2o(
            self,
            model: Type[TORTOISE_MODEL],
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> Optional[TORTOISE_MODEL]:
        o2o_data = getattr(data, field_name)
        if o2o_data is None:
            return None
        o2o_model: Type[TORTOISE_MODEL] = model._meta.fields_map[field_name].related_model
        o2o_exclude = exclude_dict[field_name]
        return await self.create(
            o2o_data,
            exclude=o2o_exclude,
            model=o2o_model,
            inside_transaction=True,
            prefix=prefix.plus(field_name)
        )

    async def create_backward_o2o(
            self,
            instance: TORTOISE_MODEL,
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_data = getattr(data, field_name)
        if back_o2o_data is None:
            return
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[TORTOISE_MODEL] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta\
            .fields_map[back_o2o_field.relation_source_field]\
            .reference.model_field_name
        back_o2o_exclude = exclude_dict[field_name]
        await self.create(
            back_o2o_data,
            exclude=back_o2o_exclude,
            model=back_o2o_model,
            defaults={back_o2o_source_field: instance},
            inside_transaction=True,
            prefix=prefix.plus(field_name)
        )

    async def create_backward_fk(
            self,
            instance: TORTOISE_MODEL,
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> None:
        list_errors = ListFieldError()
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[TORTOISE_MODEL] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        back_fk_exclude = exclude_dict[field_name]
        next_prefix = prefix.plus(field_name)
        for index, back_fk_data in enumerate(getattr(data, field_name)):
            try:
                await self.create(
                    back_fk_data,
                    exclude=back_fk_exclude,
                    model=back_fk_model,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=next_prefix,
                )
            except ObjectErrors as e:
                list_errors.append(index, e)
        if list_errors:
            raise list_errors

    async def edit(
            self,
            item_id_or_instance: PK | TORTOISE_MODEL,
            data: CamelModel,
            *,
            exclude: set[str] = None,
            background_tasks: BackgroundTasks = None,
            defaults: dict[str, Any] = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
            inside_transaction: bool = False,
            prefix: ModelPrefix = ModelPrefix(),
    ) -> TORTOISE_MODEL:
        model: Type[TORTOISE_MODEL] = item_id_or_instance.__class__ if isinstance(item_id_or_instance, BaseModel) \
            else self.model
        fk_fields, bfk_fields, o2o_fields, bo2o_fields, m2m_fields = exclude_fk_bfk_o2o_bo2o_m2m(model, data)
        exclude_dict = get_exclude_dict(exclude or set())
        errors = ObjectErrors()
        defaults = defaults or {}

        async def get_changed_instance() -> TORTOISE_MODEL:
            if isinstance(item_id_or_instance, BaseModel):
                instance = item_id_or_instance
            else:
                instance = await self.get_one(
                    item_id_or_instance,
                    request=request,
                    select_related=select_related,
                    prefetch_related=prefetch_related
                )
            not_unique = await model.check_unique(data.dict(include=model._meta.db_fields, exclude_unset=True))
            for field_name in not_unique:
                errors.add(field_name, NotUnique)
            created_o2o, picked_fks = {}, {}

            for o2o_field_name in o2o_fields:
                try:
                    o2o_instance = await self.edit_o2o(instance, o2o_field_name, data, exclude_dict, prefix=prefix)
                    if o2o_instance:
                        created_o2o[o2o_field_name] = o2o_instance
                except ObjectErrors as e:
                    errors.add(o2o_field_name, e)

            try:
                picked_fks = await self.pick_fks(model, fk_fields, data, prefix=prefix)
            except ObjectErrors as e:
                errors.merge(e)

            if errors:
                raise errors

            await self.handle_edit(instance, prefix=prefix)(
                data, should_exclude={*exclude_dict['__root__'], *fk_fields},
                defaults={**defaults, **created_o2o, **picked_fks}
            )

            for bo2o_field_name in bo2o_fields:
                try:
                    await self.edit_backward_o2o(instance, bo2o_field_name, data, exclude_dict, prefix=prefix)
                except ObjectErrors as e:
                    errors.add(bo2o_field_name, e)

            for bfk_source_field_name in bfk_fields:
                try:
                    await self.edit_backward_fk(instance, bfk_source_field_name, data, exclude_dict, prefix=prefix)
                except ListFieldError as e:
                    errors.add(bfk_source_field_name, e)

            for m2m_field_name in m2m_fields:
                await self.save_m2m(instance, data, m2m_field_name, prefix=prefix)

            if errors:
                raise errors
            return instance

        if inside_transaction:
            return await get_changed_instance()
        else:
            async with in_transaction():
                changed_instance = await get_changed_instance()
            return await self.get_one(
                changed_instance.pk,
                request=request,
                select_related=select_related,
                prefetch_related=prefetch_related,
            )

    async def edit_o2o(
            self,
            instance: TORTOISE_MODEL,
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> Optional[TORTOISE_MODEL]:
        o2o_instance = getattr(instance, field_name)
        o2o_data = getattr(data, field_name)
        o2o_exclude = exclude_dict[field_name]
        if o2o_instance is not None:
            await self.edit(
                o2o_instance,
                o2o_data,
                exclude=o2o_exclude,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )
        else:
            return await self.create(
                o2o_data,
                exclude=o2o_exclude,
                model=instance._meta.fields_map[field_name].related_model,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )

    async def edit_backward_o2o(
            self,
            instance: TORTOISE_MODEL,
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> None:
        back_o2o_instance = getattr(instance, field_name)
        back_o2o_data = getattr(data, field_name)
        back_o2o_exclude = exclude_dict[field_name]
        back_o2o_field = instance._meta.fields_map[field_name]
        back_o2o_model: Type[TORTOISE_MODEL] = back_o2o_field.related_model
        back_o2o_source_field = back_o2o_model._meta \
            .fields_map[back_o2o_field.relation_source_field] \
            .reference.model_field_name
        if back_o2o_instance is not None:
            await self.edit(
                back_o2o_instance,
                back_o2o_data,
                exclude=back_o2o_exclude,
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )
        else:
            await self.create(
                back_o2o_data,
                exclude=back_o2o_exclude,
                model=back_o2o_model,
                defaults={back_o2o_source_field: instance},
                inside_transaction=True,
                prefix=prefix.plus(field_name),
            )

    async def edit_backward_fk(
            self,
            instance: TORTOISE_MODEL,
            field_name: str,
            data: CamelModel,
            exclude_dict: dict[str, set[str]],
            prefix: ModelPrefix,
    ) -> None:
        def get_fk_instance(instances: list[TORTOISE_MODEL], pk_value) -> TORTOISE_MODEL | None:
            for i in instances:
                if i.pk == pk_value:
                    return i

        list_errors = ListFieldError()
        back_fk_instances: list[TORTOISE_MODEL] = getattr(instance, field_name)
        back_fk_field = instance._meta.fields_map[field_name]
        back_fk_model: Type[TORTOISE_MODEL] = back_fk_field.related_model
        back_fk_source_field = back_fk_model._meta \
            .fields_map[back_fk_field.relation_source_field] \
            .reference.model_field_name
        back_pk_attr = back_fk_model._meta.pk_attr
        back_o2o_exclude = exclude_dict[field_name]
        for index, back_fk_data in enumerate(getattr(data, field_name)):
            if pk := getattr(back_fk_data, back_pk_attr, None):
                fk_instance = get_fk_instance(back_fk_instances, pk)
                if fk_instance:
                    coro = self.edit(
                        fk_instance,
                        back_fk_data,
                        exclude=back_o2o_exclude,
                        inside_transaction=True,
                        prefix=prefix.plus(field_name),
                    )
                else:
                    list_errors.append(index, NotFoundFK)
                    continue
            else:
                coro = self.create(
                    back_fk_data,
                    exclude=back_o2o_exclude,
                    model=back_fk_model,
                    defaults={back_fk_source_field: instance},
                    inside_transaction=True,
                    prefix=prefix.plus(field_name),
                )
            try:
                await coro
            except ObjectErrors as e:
                list_errors.append(index, e)

        if list_errors:
            raise list_errors

    async def pick_fk(
            self,
            model: Type[TORTOISE_MODEL],
            fk_source_field_name: str,
            data: CamelModel,
            prefix: ModelPrefix,
    ) -> tuple[str, Optional[TORTOISE_MODEL]]:
        opts = model._meta
        rel_model, field_name = None, None
        for field in opts.fk_fields:
            if (f_opts := opts.fields_map[field]).source_field == fk_source_field_name:
                rel_model = f_opts.related_model
                field_name = field

        value = getattr(data, fk_source_field_name, None)
        if value is None:
            return field_name, None

        get_rel_instance_func = self.fk_get_instance_map.get(prefix.plus(fk_source_field_name), rel_model.get_or_none)
        rel_instance = await get_rel_instance_func(pk=value)
        if rel_instance is None:
            raise NotFoundFK
        return field_name, rel_instance

    async def pick_fks(
            self,
            model: Type[TORTOISE_MODEL],
            fk_fields: set[str],
            data: CamelModel,
            prefix: ModelPrefix,
    ) -> dict[str, Optional[TORTOISE_MODEL]]:
        picked_fks = {}
        errors = ObjectErrors()
        for fk_source_field_name in fk_fields:
            try:
                fk_field_name, fk_instance = await self.pick_fk(model, fk_source_field_name, data, prefix=prefix)
                picked_fks[fk_field_name] = fk_instance
            except NotFoundFK:
                errors.add(fk_source_field_name, NotFoundFK)
        if errors:
            raise errors
        return picked_fks

    async def delete_many(
            self,
            item_ids: list[PK],
            *,
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> int:
        return await self._get_many_queryset(
            item_ids,
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related,
        ).delete()

    async def delete_one(
            self,
            item_id: PK,
            *,
            background_tasks: BackgroundTasks = None,
            request: Request = None,
            select_related: Sequence[str] = (),
            prefetch_related: Sequence[str] = (),
    ) -> None:
        item = await self.get_one(
            item_id,
            background_tasks=background_tasks,
            request=request,
            select_related=select_related,
            prefetch_related=prefetch_related,
        )
        await item.delete()

    def handle_create(self, model: Type[TORTOISE_MODEL], prefix: ModelPrefix) -> Handler:
        if handler := self.create_handlers.get(prefix):
            return handler

        async def base_handler(
                data: CamelModel,
                should_exclude: set[str],
                defaults: dict[str, Any] = None,
        ) -> TORTOISE_MODEL:
            errors = ObjectErrors()
            include_fields = model._meta.db_fields.difference(should_exclude)
            data_dict = data.dict(include=include_fields, exclude_unset=True)
            if defaults is not None:
                data_dict.update(defaults)
            instance = model(**data_dict)
            opts = model._meta
            for field_name in (*opts.db_fields, *opts.fk_fields, *opts.o2o_fields):
                f_opts = opts.fields_map[field_name]
                if (
                        f_opts.null is False
                        and f_opts.pk is False
                        and getattr(instance, field_name) is None
                ):
                    errors.add(field_name, FieldRequired)
            if errors:
                raise errors
            await instance.save(force_create=True)
            return instance

        self.create_handlers[prefix] = base_handler
        return base_handler

    def handle_edit(self, instance: TORTOISE_MODEL, prefix: ModelPrefix) -> Handler:
        if handler := self.edit_handlers.get(prefix):
            return handler

        async def base_handler(
                data: CamelModel,
                should_exclude: set[str],
                defaults: dict[str, Any] = None,
        ) -> TORTOISE_MODEL:
            include_fields = instance._meta.db_fields.difference(should_exclude)
            data_dict = data.dict(include=include_fields, exclude_unset=True)
            if defaults is not None:
                data_dict.update(defaults)
            instance.update_from_dict(data_dict)
            await instance.save(force_update=True)
            return instance

        self.edit_handlers[prefix] = base_handler
        return base_handler

    async def save_m2m(
            self,
            instance: TORTOISE_MODEL,
            data: CamelModel,
            field_name: str,
            prefix: ModelPrefix,
            clear=True,
    ) -> None:
        rel: ManyToManyRelation = getattr(instance, field_name)
        ids: list[PK] = getattr(data, field_name)
        if clear:
            await rel.clear()
        await rel.add(*(await rel.remote_model.filter(pk__in=ids)))

    def get_default_sort_fields(self) -> set[str]:
        return {*self.opts.db_fields}


def get_exclude_dict(fields: set[str]) -> dict[str, set[str]]:
    """
    Из {a, b, c.d, c.e, f.g.h, f.g.i} делает
    {
        '__root__': {'a', 'b'},
        'c': {'d', 'e'},
        'f': {'g.h', 'g.i'}
    }
    """
    exclude_dict = defaultdict(set)
    for field in fields:
        if '.' not in field:
            exclude_dict['__root__'].add(field)
        else:
            base, _, field_in_related = field.partition('.')
            exclude_dict[base].add(field_in_related)
    return exclude_dict


def exclude_fk_bfk_o2o_bo2o_m2m(
        model: Type[BaseModel], data: CamelModel
) -> tuple[set[str], set[str], set[str], set[str], set[str]]:
    opts = model._meta
    return (
        exclude_fields_from_data(data, *(opts.fields_map[f].source_field for f in opts.fk_fields)),
        exclude_fields_from_data(data, *opts.backward_fk_fields),
        exclude_fields_from_data(data, *opts.o2o_fields),
        exclude_fields_from_data(data, *opts.backward_o2o_fields),
        exclude_fields_from_data(data, *opts.m2m_fields)
    )


def exclude_fields_from_data(data: CamelModel, *fields: str) -> set[str]:
    return_fields: set[str] = set()
    for field_name in fields:
        if field_name in data.__fields_set__:
            return_fields.add(field_name)
    return return_fields


def get_qs_build_func(name: str, model: Type[TORTOISE_MODEL], obj: Any):
    if obj is None:
        return getattr(model, 'get_' + name)
    else:
        if callable(obj):
            return obj
        else:
            return lambda path, method: obj
