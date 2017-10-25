from .models import SlideStack
from django.db import connection


class Structure:

    @staticmethod
    def create_structure():
        """
        This functionality checks all existing instances of SlideStack for categories and topics stored in
        categories field.
        :return: a list that contains lists. Each of the inner lists contains strings: the first element in the
        inner list is the category. All following elements in a inner list represent the topics allocated to the category
        """
        structure = []
        for slide_stack in SlideStack.objects.all().order_by('id'):
            for tup in slide_stack.list_category_tuples:
                try:
                    inner_list = next(i for i in structure if i[0].strip().lower() == tup[0].strip().lower())

                    category = inner_list.pop(0)
                    try:
                        next(it for it in inner_list if it.strip().lower() == tup[1].strip().lower())
                    except StopIteration:
                        inner_list.append(tup[1])
                    inner_list.insert(0, category)

                except StopIteration:
                    structure.append([tup[0].strip(), tup[1].strip()])

        return structure

    structure = []
    # check if table is already created before using it
    if'Slides_slidestack' in connection.introspection.table_names():
        structure = create_structure.__func__()

    @staticmethod
    def redefine_structure():
        """
        Refreshes Structure.structure after slides were added to the system.
        Should not be used, use DataStructure.redefine_data_structure() instead!
        """
        Structure.structure = Structure.create_structure()



class DataStructure:

    @staticmethod
    def create_data_structure():
        """
        This method uses the structure created with create_structure() and expands is with the matching data.
        :return: a complex data structure as follows: (String:category, [(String:topic title, [SlideStack])])
        """
        data_structure = []

        for lst in Structure.structure:
            category = lst.pop(0)

            topics = []
            for topic in lst:
                category_topic = category + '_' + topic
                slide_stacks = []
                for ss in SlideStack.objects.all():
                    if category_topic.lower() in (x.lower() for x in ss.list_categories):
                        slide_stacks.append(ss)

                topics.append((topic, slide_stacks))

            data_structure.append((category, topics))

        Structure.redefine_structure()
        return data_structure

    data_structure = []
    # check if table is already created before using it
    if 'Slides_slidestack' in connection.introspection.table_names():
        data_structure = create_data_structure.__func__()

    @staticmethod
    def redefine_data_structure():
        """
        Refreshes DataStructure.data_structure as well as Structure.structure.
        Use this method after adding slides to the system.
        :return:
        """
        DataStructure.data_structure = DataStructure.create_data_structure()
        Structure.redefine_structure()
