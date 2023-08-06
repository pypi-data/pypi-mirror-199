from typing import Optional, Union
from datetime import datetime
import json
import os
import copy

from cqlpy.types import *
from cqlpy.operators import *
from valueset_provider import ValueSetProvider


class Context:
    """
    A context is a required parameter on every CQL expression that is converted to python as a function.
    The expected signature of every function that implements a CQL Expression is:

        def EXPRESSION_NAME(context: Context):

    The Context provides access to the data model, parameter values, and value set codes as needed by the internal elements
    of a python function that implements a CQL expression. The Context provides access to these concepts via a retrieve operation
    that is implemented with syntax such as:

        context["Encounter"]    # if a string is requested (assumed to be a FHIR resource type), context returns a
                                # list of Resources from the model, in this case all Encounter resources.

        context["Encounter", ValueSet, "type"]
                                # if a tuple is requested (assumed to be a FHIR resource type), context returns a
                                # list of Resources from the model, in this case Encounter resources, filtered by
                                # checking the specified property to see if it has a coded value in the specified value set.

        context[Parameter]      # if a Parameter is requested, context returns the type specified by the Parameter
                                # with value determined by the parameter_provider from external parameters or the default value.

        context[ValueSet]       # if a ValueSet is requested, context returns a ValueSet that includes with Codes property populated
                                # from the value_set_provider.

    The Context iterates through the bundle (as a json object) to retrieve a list of Resources.

    Properties of Resources can be obtained using syntax such as:

        Encounter["period"]     # The property of the resource is properly typed when requested (in this case, Interval)
                                # by parsing the related bundle json element.

    Context Resource retrieve operations and Resource property retrieve operations are cached so that iterating through the bundle
    and parsing json is only performed once (at time of the first request).
    """

    def __init__(
        self,
        valueset_provider: ValueSetProvider,
        bundle: Optional[str] = None,
        bundle_file_name: Optional[str] = None,
        parameters: Optional[dict] = None,
    ):
        if bundle_file_name:
            with open(bundle_file_name, encoding="utf-8") as f:
                bundle = json.loads(f.read())

        self.model = FhirR4DataModel(bundle, self)

        self.cql_valueset_provider = CqlValueSetProvider(
            valueset_provider=valueset_provider
        )
        self.parameter_provider = ParameterProvider(parameters)

    def __getitem__(self, requested_concept: Union[Parameter, ValueSet, str, tuple]):
        if isinstance(requested_concept, Parameter):
            # In this case, the return type will be the Cql Type specified by the parameter,
            # i.e. Interval<DateTime>, CqlString, etc.
            return self.parameter_provider[requested_concept]

        elif isinstance(requested_concept, ValueSet):
            # In this case, the return type will be ValueSet (which includes all codes specified by the value set).
            return self.cql_valueset_provider[requested_concept]

        elif isinstance(requested_concept, Code):
            # In this case, there is nothing to lookup... the Code is fully populated.
            return requested_concept

        else:
            return self.model[requested_concept]

    def set_context(self, context: str) -> None:
        # At this time, only Patient context is supported and the context is stored without additional action.
        # The current implementation can be extended to support additional contexts by using this stored context in
        # retrieve operations (implemented in __getitem__) to filter the resources returned from the model.
        self.context = context

    def initialize(self, model, parameter_provider, cql_valueset_provider) -> None:
        self.model = model
        self.parameter_provider = parameter_provider
        self.cql_valueset_provider = cql_valueset_provider


class FhirBase:
    def __init__(self, fhir_json: object, base_type: str, context: Context):
        self._fhir_json = fhir_json
        self._base_type = base_type
        self._context = context

    def __str__(self) -> str:
        return json.dumps(self._fhir_json)

    def __getitem__(self, property_name: str):
        if property_name == "extension":
            if "extension" in self._fhir_json:
                return [
                    Element(ex, "Extension", self._context)
                    for ex in self._fhir_json["extension"]
                ]
            else:
                return []

        elif (self._base_type in FHIR_TO_CQL_TYPE_MAP) and (
            property_name in FHIR_TO_CQL_TYPE_MAP[self._base_type]
        ):
            cql_type_name = FHIR_TO_CQL_TYPE_MAP[self._base_type][property_name]

            if cql_type_name == "Choice:Interval<DateTime>":
                if f"{property_name}DateTime" in self._fhir_json:
                    value = TypeFactory.get_type(
                        "DateTime", self._fhir_json[f"{property_name}DateTime"]
                    )
                    return Interval(value, True, value, True)

            elif cql_type_name == "Reference":
                if property_name in self._fhir_json:
                    return Element(
                        self._fhir_json[property_name], "Reference", self._context
                    )
                else:
                    return Element({}, "Reference", self._context)

            elif "List<BackboneElement:" in cql_type_name:
                element_name = cql_type_name.split(":")[1].replace(">", "")

                if property_name in self._fhir_json:
                    return [
                        BackboneElement(item, element_name, self._context)
                        for item in self._fhir_json[property_name]
                    ]
                else:
                    return []

            elif "BackboneElement:" in cql_type_name:
                element_name = cql_type_name.split(":")[1]

                if property_name in self._fhir_json:
                    return BackboneElement(
                        self._fhir_json[property_name], element_name, self._context
                    )
                else:
                    return BackboneElement({}, element_name, self._context)

            elif property_name in self._fhir_json:
                return TypeFactory.get_type(
                    cql_type_name, self._fhir_json[property_name]
                )

        return Null()

    @property
    def value(self) -> str:
        return json.dumps(self._fhir_json)

    def set_property(self, property_name: str, property_value: object) -> None:
        if property_value:
            self._fhir_json[property_name] = property_value

    def get_property(self, property_name: str) -> object:
        if property_name in self._fhir_json:
            return self._fhir_json[property_name]
        else:
            return None


class Resource(FhirBase):
    def __init__(self, fhir_json: object, resource_type: str, context: Context):
        super().__init__(fhir_json, resource_type, context)

    def __getitem__(self, property_name: str):
        if "Related:" in property_name:
            resource_name = property_name.split(":")[1]

            return [
                resource
                for resource in self._model[resource_name]
                if str(self["id"]) in str(resource[self._base_type.lower()])
            ]
        else:
            return super().__getitem__(property_name)


class BackboneElement(FhirBase):
    def __init__(self, fhir_json: object, element_type: str, context: Context):
        super().__init__(fhir_json, element_type, context)


class Element(FhirBase):
    def __init__(self, fhir_json: object, element_type: str, context: Context):
        super().__init__(fhir_json, element_type, context)


class Reference(FhirBase):
    def __init__(self, fhir_json: object, context: Context):
        super().__init__(fhir_json, "Reference", context)


"""
FHIR Reference
https://github.com/CareEvolution/IOCore/tree/develop/iocore/fhir_models/R4
"""

FHIR_TO_CQL_TYPE_MAP = {
    "Condition": {
        "id": "String",
        "clinicalStatus": "Concept",
        "category": "List<Concept>",
        "code": "Concept",
        "encounter": "Reference",
        "claim": "Reference",
        "onset": "Choice:Interval<DateTime>",
        "bodySite": "List<Concept>",
    },
    "Encounter": {
        "id": "String",
        "class": "Code",
        "type": "List<Concept>",
        "period": "Interval<DateTime>",
        "status": "String",
        "diagnosis": "List<BackboneElement:Diagnosis>",
        "location": "List<BackboneElement:Location>",
        "hospitalization": "BackboneElement:EncounterHospitalization",
    },
    "Diagnosis": {
        "condition": "Reference",
    },
    "Location": {"location": "String"},
    "EncounterHospitalization": {
        "dischargeDisposition": "Concept",
    },
    "Extension": {"url": "String", "valueCoding": "Code"},
    "Reference": {"reference": "String"},
    "Patient": {
        "id": "String",
        "birthDate": "Date",
        "gender": "String",
    },
    "Procedure": {
        "encounter": "Reference",
        "claim": "Reference",
        "code": "Concept",
        "performed": "Choice:Interval<DateTime>",
        "status": "String",
    },
    "DiagnosticReport": {
        "code": "Concept",
        "effective": "Choice:Interval<DateTime>",
        "status": "String",
    },
}


class TypeFactory:
    def get_type(type_name: str, fhir_json: object = None) -> object:
        # To support the <generic> syntax, the constructor of complex types specifies the generic type as its first parameter.
        # As a result of this pattern, get_type returns an instance of the class (so it can call the constructor appropriately)
        # rather than simply returning the type.

        if "List<" in type_name:
            generic_type = NAME_TO_CQL_TYPE_MAP[type_name.split("<")[1][:-1]]

            if fhir_json:
                return [
                    TypeFactory.parse_fhir_json(generic_type, fhir_json_item)
                    for fhir_json_item in fhir_json
                ]
            else:
                return []

        elif "<" in type_name:
            generic_type = NAME_TO_CQL_TYPE_MAP[type_name.split("<")[1][:-1]]
            type_name = type_name.split("<")[0]

            if fhir_json:
                return NAME_TO_CQL_TYPE_MAP[type_name](
                    generic_type=generic_type
                ).parse_fhir_json(fhir_json)
            else:
                return NAME_TO_CQL_TYPE_MAP[type_name](generic_type=generic_type)

        else:
            return TypeFactory.parse_fhir_json(
                NAME_TO_CQL_TYPE_MAP[type_name], fhir_json
            )

    def parse_fhir_json(return_type: object, fhir_json: object) -> object:
        if return_type == bool:
            return (
                str(fhir_json).lower().replace('"', "").replace("'", "").strip()
                == "true"
            )

        elif return_type == float:
            return float(fhir_json)

        elif return_type == int:
            return int(fhir_json)

        elif return_type == str:
            return str(fhir_json)

        else:
            return return_type().parse_fhir_json(fhir_json)


NAME_TO_CQL_TYPE_MAP = {
    "Boolean": bool,
    "Code": Code,
    "Concept": Concept,
    "Date": Date,
    "DateTime": DateTime,
    "Decimal": float,
    "Integer": int,
    "Interval": Interval,
    "List": list,
    "String": str,
}


class FhirR4DataModel:
    def __init__(self, bundle: dict, context: Context) -> None:
        self.context = context
        self.resource_id_index = {}
        self.resource_type_index = {}
        self.retrieve_cache = {}

        if "entry" in bundle:
            for entry in bundle["entry"]:
                if (
                    ("resource" in entry)
                    and ("resourceType" in entry["resource"])
                    and ("id" in entry["resource"])
                ):
                    resource_json = entry["resource"]
                    resource_type = entry["resource"]["resourceType"]
                    resource_id = f"{resource_type}/{entry['resource']['id']}"

                    self.resource_id_index[resource_id] = resource_json
                    if not (resource_type in self.resource_type_index):
                        self.resource_type_index[resource_type] = [resource_id]
                    else:
                        self.resource_type_index[resource_type].append(resource_id)

    def __getitem__(self, resource_query: Union[str, tuple]) -> list:
        duration_start_time = datetime.now()

        if type(resource_query) == tuple:
            resource_type = resource_query[0]  # expected type: str
            filter = (
                resource_query[1] if len(resource_query) > 1 else None
            )  # expected type: ValueSet or list[Code] or Code
            property_name = (
                resource_query[2] if len(resource_query) > 1 else None
            )  # expected type: str

        else:
            resource_type = resource_query
            filter = None
            property_name = None

        resource_type = (
            resource_type[resource_type.index("}") + 1 :]
            if "}" in resource_type
            else resource_type
        )

        resources = []
        filter_codes = []
        filter_property_map = {}
        filter_name = ""

        if isinstance(filter, ValueSet):
            filter_name = f"filter on ValueSet: {filter.name}"
            filter_codes = filter.codes
        elif isinstance(filter, Code):
            filter_name = f"filter on Code: {filter.code} {str(filter.system)}"
            filter_codes = [filter]
        elif isinstance(filter, list):
            filter_name = "filter on list"
            filter_codes = filter

        if filter and filter in self.retrieve_cache:
            print(
                f"retrieve from cache duration={(datetime.now() - duration_start_time).total_seconds()} resourceType={resource_type} filter={filter_name}"
            )
            return self.retrieve_cache[filter]

        if self.context[Parameter("strict", "str")] == "True":
            filter_property_map[resource_type] = property_name
        else:
            added_code_systems = []

            for code in filter_codes:
                if not code.system in added_code_systems:
                    added_code_systems.append(code.system)

                    if code.system in FILTER_PROPERTY_PROXIES:
                        filter_properties = FILTER_PROPERTY_PROXIES[code.system]
                        for resource_type_filter in filter_properties:
                            filter_property_map[
                                resource_type_filter
                            ] = filter_properties[resource_type_filter]

            if not resource_type in filter_property_map:
                filter_property_map[resource_type] = property_name

        if filter is None:
            if resource_type in self.resource_type_index:
                for id in self.resource_type_index[resource_type]:
                    resources.append(
                        Resource(
                            self.resource_id_index[id], resource_type, self.context
                        )
                    )

        else:
            for resource_type_filter in filter_property_map:
                if resource_type_filter in self.resource_type_index:
                    for id in self.resource_type_index[resource_type_filter]:
                        resource = Resource(
                            self.resource_id_index[id],
                            resource_type_filter,
                            self.context,
                        )

                        resource_property_filter = filter_property_map[
                            resource_type_filter
                        ]

                        resource_property = resource[resource_property_filter]

                        if isinstance(resource_property, list):
                            for concept in resource_property:
                                if exists(intersect(concept.codes, filter_codes)):
                                    resources.append(resource)

                        elif isinstance(resource_property, Code) and in_list(
                            resource_property, filter_codes
                        ):
                            resources.append(resource)

                        elif isinstance(resource_property, Concept) and exists(
                            intersect(resource_property.codes, filter_codes)
                        ):
                            resources.append(resource)

        if self.context[Parameter("strict", "str")] == "True":
            print(
                f"retrieve strict=True resources={len(resources)} duration={(datetime.now() - duration_start_time).total_seconds()} resourceType={resource_type} filter={filter_name}"
            )

            self.retrieve_cache[filter] = resources

            return resources
        else:
            resource_proxies = []

            for resource in resources:
                if resource._base_type == resource_type:
                    resource_proxies.append(resource)

                # special handling for the case 1) Procedure or Condition matched a filter, but 2) an Encounter was requested
                elif (
                    resource._base_type in ["Procedure", "Condition", "Observation"]
                    and (resource_type == "Encounter")
                    and not is_null(resource["encounter"]["reference"])
                    and (resource["encounter"]["reference"] in self.resource_id_index)
                ):
                    # possibility 1: Procedure or Encounter reference an Encounter- look up the Encounter and return it
                    related_encounter_resouce = Resource(
                        self.resource_id_index[resource["encounter"]["reference"]],
                        "Encounter",
                        self.context,
                    )
                    related_encounter_resouce.set_property("status", "finished")
                    resource_proxies.append(related_encounter_resouce)

                else:
                    resource_proxies.append(
                        self._generate_resource_proxy(resource, resource_type)
                    )

            print(
                f"retrieve resources={len(resource_proxies)} duration={(datetime.now() - duration_start_time).total_seconds()} resourceType={resource_type} filter={filter_name}"
            )

            self.retrieve_cache[filter] = resource_proxies

            return resource_proxies

    def _generate_resource_proxy(self, resource: object, preferred_type: str) -> object:
        resource_translation = f"{preferred_type}~{resource._base_type}"

        proxy_resource = Resource(
            json.loads(json.dumps(resource._fhir_json)),
            preferred_type,
            resource._context,
        )
        proxy_resource._base_type = preferred_type
        proxy_resource.set_property("derivedFromResourceType", resource._base_type)
        proxy_resource.set_property("resourceType", preferred_type)

        proxy_properties = {}
        if resource_translation in RESOURCE_PROXIES:
            proxy_properties = RESOURCE_PROXIES[resource_translation]

        for property in proxy_properties:
            if "literal:" in proxy_properties[property]:
                proxy_resource.set_property(
                    property, proxy_properties[property].replace("literal:", "")
                )
            elif "period:" in proxy_properties[property]:
                proxy_resource.set_property(
                    property,
                    {
                        "start": resource.get_property(
                            proxy_properties[property].replace("period:", "")
                        )
                    },
                )
            else:
                proxy_resource.set_property(
                    property, resource.get_property(proxy_properties[property])
                )

        return proxy_resource


FILTER_PROPERTY_PROXIES = {
    "cpt": {"Procedure": "code", "Encounter": "type"},
    "http://www.ama-assn.org/go/cpt": {"Procedure": "code", "Encounter": "type"},
    "https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets": {
        "Procedure": "code",
        "Encounter": "type",
    },
    "http://loinc.org": {"Observation": "code", "DiagnosticReport": "type"},
    "http://snomed.info/sct": {"Condition": "code", "DiagnosticReport": "type"},
}


RESOURCE_PROXIES = {
    "DiagnosticReport~Procedure": {
        "effectiveDateTime": "performedDateTime",
        "status": "literal:final",
    },
    "Encounter~Procedure": {
        "period": "period:performedDateTime",
        "status": "literal:finished",
    },
}


class ParameterProvider:
    def __init__(self, parameters: dict) -> None:
        self.__parameters = parameters if parameters else {}

    def __getitem__(self, parameter: Parameter):
        if parameter.name in self.__parameters:
            parameter_value = self.__parameters[parameter.name]

            cql_type = TypeFactory.get_type(parameter.type_name)
            cql_type.parse_cql(parameter_value)

            return cql_type
        else:
            if parameter.default_value:
                cql_type = TypeFactory.get_type(parameter.type_name)
                cql_type.parse_cql(parameter.default_value)

                return cql_type
            else:
                return None


class CqlValueSetProvider:
    def __init__(self, valueset_provider: ValueSetProvider) -> None:
        self._valueset_provider = valueset_provider

    def __getitem__(self, value_set: ValueSet) -> ValueSet:
        name = value_set.id.replace("http://cts.nlm.nih.gov/fhir/ValueSet/", "")

        result = self._valueset_provider.get_valueset(name=name)

        if result:
            return value_set.parse_fhir_json(result)

        print(f"value set 'scopeless:{value_set.name}' not found")

        return value_set
