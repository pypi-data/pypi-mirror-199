from rest_framework import serializers, viewsets
from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer
from .models import Application, Federation, ApplicationComponent
from djangoldp_component.models import Component, Package


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ("slug", "deploy")


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ("slug", "deploy")


class ApplicationDetailSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, obj):
        application = super().to_representation(obj)

        federation = []
        for host in application["federation"]:
            federation.append(Federation.objects.get(urlid=host).target.api_url)

        serialized = {"apps": {"hosts": {}}}
        serialized["apps"]["hosts"][application["slug"]] = {
            "graphics": {
                "client": application["client_url"],
                "title": application["application_title"],
                "canva": application["repository"],
                "logo": application["application_logo"],
            },
            "data": {"api": application["api_url"], "with": federation},
            "packages": [],
            "components": [],
        }

        for applicationComponent in application["components"]:
            component = Component.objects.get(id=applicationComponent.obj.component_id)
            insertComponent = {"type": component.name, "parameters": []}
            keys = []
            for parameter in applicationComponent.obj.parameters.all():
                insertComponent["parameters"].append(
                    {
                        "key": parameter.key,
                        "value": parameter.value,
                    }
                )
                keys.append(parameter.key)
            for parameter in component.parameters.all():
                if not parameter.key in keys:
                    insertComponent["parameters"].append(
                        {
                            "key": parameter.key,
                            "value": parameter.default,
                        }
                    )
            serialized["apps"]["hosts"][application["slug"]]["components"].append(
                insertComponent
            )

        for applicationPackage in application["packages"]:
            package = Package.objects.get(id=applicationPackage.obj.package_id)
            insertDependency = {
                "distribution": package.distribution,
                "module": package.module,
                "parameters": [],
            }
            keys = []
            for parameter in applicationPackage.obj.parameters.all():
                insertDependency["parameters"].append(
                    {
                        "key": parameter.key,
                        "value": parameter.value,
                    }
                )
                keys.append(parameter.key)
            for parameter in package.parameters.all():
                if not parameter.key in keys:
                    insertDependency["parameters"].append(
                        {
                            "key": parameter.key,
                            "value": parameter.default,
                        }
                    )
            serialized["apps"]["hosts"][application["slug"]]["packages"].append(
                insertDependency
            )

        return serialized

    class Meta:
        model = Application
        lookup_field = "slug"
        fields = [
            "urlid",
            "slug",
            "api_url",
            "client_url",
            "application_title",
            "application_logo",
            "components",
            "packages",
            "repository",
            "federation",
        ]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)


class ApplicationDetailViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    lookup_field = "slug"
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)
