from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import Aurora, Dynamodb
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.custom import Custom
# from diagrams.onprem.monitoring import NewRelic
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import Users

with Diagram("Web Application Architecture", show=False):
    with Cluster("Public Facing Network"):
        waf = EC2("WAF")
        alb = ELB("ALB")
        webserver = Nginx("Webserver")
        waf - alb
        alb - webserver

    with Cluster("Private Network"):
        msa1 = EC2("MSA1")
        msa2 = EC2("MSA2")
        msa3 = EC2("MSA3")
        aurora = Aurora("Aurora PostgreSQL")
        dynamodb = Dynamodb("DynamoDB")
        elasticache = Custom("ElasticCache Redis", "/path/to/elaticcache.png")
        s3 = S3("S3")
        msa1 - dynamodb
        msa2 - dynamodb
        msa3 - aurora
        msa3 - s3

    with Cluster("Monitoring & Logging"):
        elk = Custom("ELK Elasticsearch", "/path/to/elasticsearch.png")
#         newrelic = NewRelic("New Relic")
#         elk - newrelic

    waf - alb
    alb - webserver
    webserver >> msa1
    webserver >> msa2
    webserver >> msa3
    msa1 >> dynamodb
    msa2 >> dynamodb
    msa3 >> aurora
    msa3 >> s3
    elasticache >> msa2
    s3 >> msa3
#     dynamodb - newrelic
#     aurora - newrelic

    users = Users("Users")
    users >> webserver

