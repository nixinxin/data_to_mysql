from django.db import models

# Create your models here.


class WheatFamilyData(models.Model):
    """
    小麦系谱数据库
    """
    id = models.IntegerField(primary_key=True, verbose_name='顺序号')
    unit_id = models.IntegerField(verbose_name='品资所编号')
    name = models.CharField(max_length=40, verbose_name='品种名称')
    family = models.CharField(max_length=100, verbose_name='系谱')
    original_name = models.CharField(max_length=40, verbose_name='原名')
    source = models.CharField(max_length=40, verbose_name='来源')
    original_addr = models.CharField(max_length=40, verbose_name='原产地')
    unit = models.CharField(max_length=40, verbose_name='选育单位')
    height = models.IntegerField(null=True, blank=True, verbose_name='株高')
    qian_weight = models.CharField(max_length=6, null=True, blank=True, verbose_name='千粒重')
    year = models.CharField(max_length=6, null=True, blank=True, verbose_name='选育年限')
    comment = models.CharField(max_length=40, verbose_name='备注')

    class Meta:
        verbose_name = "小麦系谱数据库"
        verbose_name_plural = verbose_name
        db_table = "小麦系谱数据库"

    def __str__(self):
        # 不要返回name,它可能为空，导致登陆报错
        return self.name


class ResourcesFromaBroad(models.Model):
    """
    国外引进作物种质资源数据库
    """
    total_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='总编号')
    import_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='引种编号')
    copes_category = models.CharField(max_length=20, null=True, blank=True, verbose_name='作物类别')
    copes_type = models.CharField(max_length=20,  null=True, blank=True, verbose_name='作物种类')
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='作物名称')
    category_name = models.CharField(max_length=110,  null=True, blank=True, verbose_name='品种名称')
    translated_name = models.CharField(max_length=40,  null=True, blank=True, verbose_name='译名')
    source = models.CharField(max_length=30, null=True, blank=True, verbose_name='来源地')
    source_area = models.CharField(max_length=40, null=True, blank=True, verbose_name='原产地')
    total_way = models.CharField(max_length=40, null=True, blank=True, verbose_name='总途径')
    import_way = models.CharField(max_length=40, null=True, blank=True, verbose_name='引入途径')
    import_year = models.CharField(max_length=40, null=True, blank=True, verbose_name='引入年份')
    import_time = models.CharField(max_length=40, null=True, blank=True, verbose_name='引入时间')
    distribution_unit = models.CharField(max_length=60, null=True, blank=True, verbose_name='分发单位')
    feature = models.CharField(max_length=40, null=True, blank=True, verbose_name='特征特性')
    Save_unit = models.CharField(max_length=40, null=True, blank=True, verbose_name='保存单位')
    comment = models.CharField(max_length=40, null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = "国外引进作物种质资源数据库"
        verbose_name_plural = verbose_name
        db_table = verbose_name

    def __str__(self):
        return self.name
