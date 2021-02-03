BOT_NAME = 'societegenerale'
SPIDER_MODULES = ['societegenerale.spiders']
NEWSPIDER_MODULE = 'societegenerale.spiders'
LOG_LEVEL = 'WARNING'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {
   'societegenerale.pipelines.DatabasePipeline': 300,
}
