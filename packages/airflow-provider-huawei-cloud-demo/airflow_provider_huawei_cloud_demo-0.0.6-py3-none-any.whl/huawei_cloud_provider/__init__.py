__name__ = "airflow-provider-huawei-cloud-demo"

def get_provider_info():
    return {
        "package-name": __name__,  # Required
        "name": "Huawei Cloud Apache Airflow Provider",  # Required
        "description": "Huawei Cloud Apache Airflow Provider",  # Required
        "connection-types": [
            {
                "connection-type": "huaweicloud",
                "hook-class-name": "huawei_cloud_provider.hooks.base_huawei_cloud.HuaweiBaseHook",
            }
        ],
        # "extra-links": ["huawei_cloud_provider.operators.sample.SampleOperatorExtraLink"],
        "versions": ["0.0.6"],  # Required
    }
