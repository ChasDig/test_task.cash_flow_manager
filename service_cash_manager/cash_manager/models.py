from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    """Mixin - ID(UUID)."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class DatetimeStampedMixin(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Время создания сущности",
    )

    class Meta:
        abstract = True


class CashFlowSubCategory(UUIDMixin):
    """Модель - Подкатегория движения денежного средства (ДДС)."""

    title = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование подкатегории (ru)",
    )
    alias = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование подкатегории (en)",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_subcategory'
        verbose_name = "Подкатегория ДДС"
        verbose_name_plural = "Подкатегории ДДС"

    def __str__(self) -> str:
        return f"SubCategoryTitle={self.title}(Alias={self.alias})"


class CashFlowCategory(UUIDMixin):
    """Модель - Категория движения денежного средства (ДДС)."""

    title = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование категории (ru)",
    )
    alias = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование категории (en)",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_category'
        verbose_name = "Категория ДДС"
        verbose_name_plural = "Категории ДДС"

    def __str__(self) -> str:
        return f"CategoryTitle={self.title}(Alias={self.alias})"


class CashFlowCategoryBySubcategory(UUIDMixin):
    """
    Модель-связка - отношение Категории к Подкатегории
    движения денежного средства (ДДС).
    """

    category = models.ForeignKey(
        "CashFlowCategory",
        on_delete=models.CASCADE,
        related_name="category_by_subcategory",
    )
    subcategory = models.ForeignKey(
        "CashFlowSubCategory",
        on_delete=models.CASCADE,
        related_name="category_by_subcategory",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_category_by_subcategory'
        verbose_name = "Связка Категории и Подкатегории ДДС"
        verbose_name_plural = "Связки Категорий и Подкатегорий ДДС"

    def __str__(self) -> str:
        return f"CategoryID={self.category}, SubCategoryID={self.subcategory})"


class CashFlowType(UUIDMixin):
    """Модель - Тип движения денежного средства (ДДС)."""

    title = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование типа (ru)",
    )
    alias = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование типа (en)",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_type'
        verbose_name = "Тип ДДС"
        verbose_name_plural = "Типы ДДС"

    def __str__(self) -> str:
        return f"TypeTitle={self.title}(Alias={self.alias})"


class CashFlowCategoryByType(UUIDMixin):
    """
    Модель-связка - отношение Категории к типу
    движения денежного средства (ДДС).
    """

    category = models.ForeignKey(
        "CashFlowCategory",
        on_delete=models.CASCADE,
        related_name="category_by_type",
    )
    type = models.ForeignKey(
        "CashFlowType",
        on_delete=models.CASCADE,
        related_name="category_by_type",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_category_by_type'
        verbose_name = "Связка Категории и Типа ДДС"
        verbose_name_plural = "Связки Категорий и Подкатегорий ДДС"

    def __str__(self) -> str:
        return f"CategoryID={self.category}, TypeID={self.type})"


class CashFlowStatus(UUIDMixin):
    """Модель - Статус движения денежного средства (ДДС)."""

    title = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование статуса (ru)",
    )
    alias = models.CharField(
        max_length=256,
        null=False,
        unique=True,
        help_text="Наименование статуса (en)",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow_status'
        verbose_name = "Статус ДДС"
        verbose_name_plural = "Статусы ДДС"

    def __str__(self) -> str:
        return f"StatusTitle={self.title}(Alias={self.alias})"


class CashFlow(UUIDMixin, DatetimeStampedMixin):
    """Модель - Движение денежного средства (ДДС)."""

    status = models.ForeignKey(
        "CashFlowStatus",
        on_delete=models.PROTECT,
        related_name="cash_flow",
    )
    type = models.ForeignKey(
        "CashFlowType",
        on_delete=models.PROTECT,
        related_name="cash_flow",
    )

    amount = models.DecimalField(
        max_digits=11,
        decimal_places=3,
        null=False,
        help_text="Кол-во денежных средств в рублях",
    )
    comment = models.CharField(
        max_length=512,
        null=True,
        help_text="Комментарий",
    )

    class Meta:
        db_table = 'cash_manager"."cash_flow'
        verbose_name = "Движение денежного средства"
        verbose_name_plural = "Движения денежных средств"

    def __str__(self) -> str:
        return f"CashFlowID={self.id}"
