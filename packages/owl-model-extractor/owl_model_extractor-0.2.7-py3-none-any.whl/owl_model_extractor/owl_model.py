import requests
import rdflib
from rdflib.plugin import register, Parser
from owlready2 import *
from owl_model_extractor import owl_model_extractor_constants_values as constants


class OwlModel:
    __ontology: Ontology
    is_loaded: bool

    def __init__(self, ontology_url):
        try:
            for format_element in constants.FORMATS_DEFINITION:
                if self.validateFormat(format=format_element, ontology_url=ontology_url):
                    self.is_loaded = True
                    break
                else:
                    self.is_loaded = False
        except Exception as ex:
            print("ERROR Loading file")

    def validateFormat(self, format, ontology_url):
        my_world = World()
        f_name = ontology_url[(ontology_url.rindex("/")) + 1:] + ".rdf"
        register(constants.PUGLIN_DEFINITION[format], Parser, constants.FORMATS_DEFINITION[format],
                 constants.PARSER_DEFINITION[format])
        try:
            g = rdflib.Graph()
            g.parse(ontology_url, format=constants.FORMATS_DEFINITION[format])
            g.serialize(destination=f_name, format="application/rdf+xml")
            self.__ontology = my_world.get_ontology(f_name).load()
            if str(self.__ontology.base_iri).endswith("#"):
                if self.__ontology.base_iri[:-1].__eq__(f_name):
                    self.__ontology.base_iri = ontology_url
            else:
                if self.__ontology.base_iri.__eq__(f_name):
                    self.__ontology.base_iri = ontology_url
            os.remove(f_name)
            return True
        except Exception as ex:
            return False

    def get_base_iri(self):
        if hasattr(self.__ontology, "base_iri"):
            return self.__ontology.base_iri
        else:
            return ""

    def get_license(self):
        license_list = []
        for license in constants.LICENSE:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if license.__eq__(metadata):
                        license_list = list(
                            self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", license),
                                                         error_on_undefined_entities=False))
                        if license_list and license_list[0]:
                            if license_list[0][0]:
                                if license_list[0][0].iri.__eq__(self.__ontology.base_iri):
                                    return license_list[0][1]
                                elif license_list[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return license_list[0][1]
                                elif license_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                                    return license_list[0][1]
                                elif license_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return license_list[0][1]
                                if license_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                                    return license_list[0][1]
                                elif license_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return license_list[0][1]
                                elif license_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                                    return license_list[0][1]
                                elif license_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return license_list[0][1]
                        else:
                            return None
                elif isinstance(metadata, AnnotationPropertyClass):
                    if license.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.license

        if not license_list:
            for license in constants.LICENSE:
                license_list = list(
                    self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", license),
                                                 error_on_undefined_entities=False))
                if license_list and license_list[0]:
                    if license_list[0][0]:
                        if license_list[0][0].iri.__eq__(self.__ontology.base_iri):
                            return license_list[0][1]
                        elif license_list[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                            return license_list[0][1]
                        elif license_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                            return license_list[0][1]
                        elif license_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return license_list[0][1]
                        if license_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                            return license_list[0][1]
                        elif license_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                            return license_list[0][1]
                        elif license_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                            return license_list[0][1]
                        elif license_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return license_list[0][1]
                else:
                    return None

    def get_preferred_namespace_prefix(self):
        preferredPrefix = []
        for namespace_prefix in constants.PREFERRED_PREFIX:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if namespace_prefix.__eq__(metadata):
                        preferredPrefix = list(
                            self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_prefix),
                                                         error_on_undefined_entities=False))
                        if preferredPrefix and preferredPrefix[0]:
                            if preferredPrefix[0][0]:
                                if preferredPrefix[0][0].iri.__eq__(self.__ontology.base_iri):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return preferredPrefix[0][1]
                                if preferredPrefix[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                                    return preferredPrefix[0][1]
                                elif preferredPrefix[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return preferredPrefix[0][1]

                        else:
                            return None
                elif isinstance(metadata, AnnotationPropertyClass):
                    if namespace_prefix.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.preferredNamespacePrefix
        if not preferredPrefix:
            for namespace_prefix in constants.PREFERRED_PREFIX:
                preferredPrefix = list(
                    self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_prefix),
                                                 error_on_undefined_entities=False))
                if preferredPrefix and preferredPrefix[0]:
                    if preferredPrefix[0][0]:
                        if preferredPrefix[0][0].iri.__eq__(self.__ontology.base_iri):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return preferredPrefix[0][1]
                        if preferredPrefix[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                            return preferredPrefix[0][1]
                        elif preferredPrefix[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return preferredPrefix[0][1]
                else:
                    return None

    def get_preferred_namespace_uri(self):
        namespace_uri_list = []
        for namespace_uri in constants.PREFERRED_PREFIX:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if namespace_uri.__eq__(metadata):
                        namespace_uri_list = list(
                            self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_uri),
                                                         error_on_undefined_entities=False))
                        if namespace_uri_list and namespace_uri_list[0]:
                            if namespace_uri_list[0][0]:
                                if namespace_uri_list[0][0].iri.__eq__(self.__ontology.base_iri):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return namespace_uri_list[0][1]
                                if namespace_uri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                                    return namespace_uri_list[0][1]
                                elif namespace_uri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                                    return namespace_uri_list[0][1]

                        else:
                            return None
                elif isinstance(metadata, AnnotationPropertyClass):
                    if namespace_uri.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.preferredNamespaceUri

        if not namespace_uri_list:
            for namespace_uri in constants.PREFERRED_PREFIX:
                namespace_uri_list = list(
                    self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_uri),
                                                 error_on_undefined_entities=False))
                if namespace_uri_list and namespace_uri_list[0]:
                    if namespace_uri_list[0][0]:
                        if namespace_uri_list[0][0].iri.__eq__(self.__ontology.base_iri):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return namespace_uri_list[0][1]
                        if namespace_uri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                            return namespace_uri_list[0][1]
                        elif namespace_uri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                            return namespace_uri_list[0][1]
                else:
                    return None

    def get_version_iri(self):
        for version_iri in constants.VERSION:
            version_iri_list = list(
                self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", version_iri),
                                             error_on_undefined_entities=False))
            if version_iri_list and version_iri_list[0]:
                if version_iri_list[0][0]:
                    if version_iri_list[0][0].iri.__eq__(self.__ontology.base_iri):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].iri.__eq__(self.__ontology.base_iri[:-1]):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                        return version_iri_list[0][1]
                    if version_iri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].namespace.base_iri.__eq__(self.__ontology.base_iri[:-1]):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri):
                        return version_iri_list[0][1]
                    elif version_iri_list[0][0].namespace.base_iri[:-1].__eq__(self.__ontology.base_iri[:-1]):
                        return version_iri_list[0][1]
            else:
                return None

    def get_metadata_as_iri_list(self) -> list:
        metadata_list = []
        # Extract metadata from Ontology Object
        query = constants.SPARQL_METADATA_EXTRACT
        query = query.replace("##PH1##", self.__ontology.base_iri)
        for metadata in self.__ontology.metadata:
            if isinstance(metadata, AnnotationPropertyClass):
                metadata_list.append(metadata.namespace.base_iri + metadata.name)
            elif isinstance(metadata, str):
                metadata_list.append(metadata)

        # Extract annotation_properties from OWL
        for item in self.__ontology.annotation_properties():
            metadata_list.append(item.namespace.base_iri + item.name)

        if str(self.__ontology.base_iri).endswith("#") or str(self.__ontology.base_iri).endswith("/"):
            # Extract Metadata from Sparql query
            graph = self.__ontology.world.as_rdflib_graph()
            list_metadata = list(
                graph.query(query))
            for metadata in list_metadata:
                for m in metadata:
                    metadata_list.append(str(m))

            query = constants.SPARQL_METADATA_EXTRACT
            query = query.replace("##PH1##", self.__ontology.base_iri[:-1])

            # Extract Metadata from Sparql query
            graph = self.__ontology.world.as_rdflib_graph()
            list_metadata = list(
                graph.query(query))
            for metadata in list_metadata:
                for m in metadata:
                    metadata_list.append(str(m))
        else:
            # Extract Metadata from Sparql query
            graph = self.__ontology.world.as_rdflib_graph()
            list_metadata = list(
                graph.query(query))
            for metadata in list_metadata:
                for m in metadata:
                    metadata_list.append(str(m))
        return metadata_list

    def get_namespace(self) -> str:
        return self.__ontology.get_namespace(self.__ontology.base_iri)

    def get_reuse_vocab_terms(self) -> list:
        reuse_vocab_terms = []
        for classes in self.__ontology.classes():
            if not classes.iri.__str__().startswith(constants.NS_OWL) and not classes.namespace.base_iri.__eq__(
                    self.__ontology.base_iri):
                reuse_vocab_terms.append(classes.namespace.base_iri)
        for obj_property in self.__ontology.object_properties():
            if not obj_property.iri.__str__().startswith(
                    constants.NS_OWL) and not obj_property.namespace.base_iri.__eq__(
                self.__ontology.base_iri):
                reuse_vocab_terms.append(obj_property.namespace.base_iri)
        for data_property in self.__ontology.data_properties():
            if not data_property.iri.__str__().startswith(
                    constants.NS_OWL) and not data_property.namespace.base_iri.__eq__(
                self.__ontology.base_iri):
                reuse_vocab_terms.append(data_property.namespace.base_iri)
        return reuse_vocab_terms

    def get_classes(self) -> list:
        classes_list = []
        for classes in self.__ontology.classes():
            if not classes.iri.__str__().startswith(constants.NS_OWL):
                classes_list.append(classes)
        return classes_list

    def get_object_properties(self) -> list:
        obj_property_list = []
        for obj_property in self.__ontology.object_properties():
            if not obj_property.iri.__str__().startswith(constants.NS_OWL):
                obj_property_list.append(obj_property)
        return obj_property_list

    def get_data_properties(self) -> list:
        data_property_list = []
        for data_property in self.__ontology.data_properties():
            if not data_property.iri.__str__().startswith(constants.NS_OWL):
                data_property_list.append(data_property)
        return data_property_list

    def get_base_classes(self) -> list:
        classes_list = []
        for classes in self.__ontology.classes():
            if not classes.iri.__str__().startswith(constants.NS_OWL) and classes.namespace.base_iri.__eq__(
                    self.__ontology.base_iri):
                classes_list.append(classes)
        return classes_list

    def get_base_object_properties(self) -> list:
        obj_property_list = []
        for obj_property in self.__ontology.object_properties():
            if not obj_property.iri.__str__().startswith(constants.NS_OWL) and obj_property.namespace.base_iri.__eq__(
                    self.__ontology.base_iri):
                obj_property_list.append(obj_property)
        return obj_property_list

    def get_base_data_properties(self) -> list:
        data_property_list = []
        for data_property in self.__ontology.data_properties():
            if not data_property.iri.__str__().startswith(constants.NS_OWL) and data_property.namespace.base_iri.__eq__(
                    self.__ontology.base_iri):
                data_property_list.append(data_property)
        return data_property_list

    def get_classes_with_label(self):
        list_classes_with_label = []
        for term in self.get_base_classes():
            if term.label is not None and len(term.label) > 0:
                list_classes_with_label.append(term)
        return len(list_classes_with_label)

    def get_object_properties_with_label(self):
        list_obj_with_label = []
        for term in self.get_base_object_properties():
            if term.label is not None and len(term.label) > 0:
                list_obj_with_label.append(term)
        return len(list_obj_with_label)

    def get_data_properties_with_label(self):
        list_data_with_label = []
        for term in self.get_base_data_properties():
            if term.label is not None and len(term.label) > 0:
                list_data_with_label.append(term)
        return len(list_data_with_label)

    def get_classes_with_description(self):
        list_classes_with_description = []
        for term in self.get_base_classes():
            if term.comment is not None and len(term.comment) > 0:
                list_classes_with_description.append(term)
        return len(list_classes_with_description)

    def get_object_properties_with_description(self):
        list_obj_with_description = []
        for term in self.get_base_object_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_obj_with_description.append(term)
        return len(list_obj_with_description)

    def get_data_properties_with_description(self):
        list_data_with_description = []
        for term in self.get_base_data_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_data_with_description.append(term)
        return len(list_data_with_description)

    def get_imported_ontologies(self):
        imported_ontologies = []
        for imported in self.__ontology.imported_ontologies:
            imported_ontologies.append(imported.base_iri)
        return imported_ontologies
