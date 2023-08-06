__name__ = "airflow-provider-huawei-cloud"

def get_provider_info():
    return {
        "package-name": __name__,  # Required
        "name": "Huawei Cloud Apache Airflow Provider",  # Required
        "description": "A sample template for Apache Airflow providers.",  # Required
        "connection-types": [
            {
                "connection-type": "huaweicloud",
                "hook-class-name": "huawei_cloud_provider.hooks.base_huawei_cloud.HuaweiBaseHook",
            }
        ],
        "extra-links": ["huawei_cloud_provider.operators.sample.SampleOperatorExtraLink"],
        "versions": ["0.0.4"],  # Required
    }
