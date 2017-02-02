from .models import SlideStack
from Course.models import Course


class GsiStructure:

    @staticmethod
    def create_structure():
        """
        This functionality checks all existing instances of SlideStack for categories and topics stored in
        categories field.
        :return: a list that contains lists. Each of the inner lists contains strings: the first element in the
        inner list is the category. All following elements in a inner list represent the topics allocated to the category
        """
        structure = []
        for slide_stack in SlideStack.objects.filter(course=Course.objects.get(short_title='gsi')):
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

    structure = create_structure.__func__()

    @staticmethod
    def redefine_structure():
        """
        Refreshes Structure.structure after slides were added to the system.
        Should not be used, use DataStructure.redefine_data_structure() instead!
        """
        __class__.structure = __class__.create_structure()


class GsiDataStructure:

    @staticmethod
    def create_data_structure():
        """
        This method uses the structure created with create_structure() and expands is with the matching data.
        :return: a complex data structure as follows: (String:category, [(String:topic title, [SlideStack])])
        """
        data_structure = []

        for lst in GsiStructure.structure:
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

        GsiStructure.redefine_structure()
        return data_structure

    data_structure = create_data_structure.__func__()

    @staticmethod
    def redefine_data_structure():
        """
        Refreshes DataStructure.data_structure as well as Structure.structure.
        Use this method after adding slides to the system.
        :return:
        """
        __class__.data_structure = __class__.create_data_structure()
        GsiStructure.redefine_structure()


class HciStructure:

    @staticmethod
    def create_structure():
        """
        This functionality checks all existing instances of SlideStack for categories and topics stored in
        categories field.
        :return: a list that contains lists. Each of the inner lists contains strings: the first element in the
        inner list is the category. All following elements in a inner list represent the topics allocated to the category
        """
        structure = []
        for slide_stack in SlideStack.objects.filter(course=Course.objects.get(short_title='hci')):
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

    structure = create_structure.__func__()

    @staticmethod
    def redefine_structure():
        """
        Refreshes Structure.structure after slides were added to the system.
        Should not be used, use DataStructure.redefine_data_structure() instead!
        """
        HciStructure.structure = HciStructure.create_structure()


class HciDataStructure:

    @staticmethod
    def create_data_structure():
        """
        This method uses the structure created with create_structure() and expands is with the matching data.
        :return: a complex data structure as follows: (String:category, [(String:topic title, [SlideStack])])
        """
        data_structure = []

        for lst in HciStructure.structure:
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

        HciStructure.redefine_structure()
        return data_structure

    data_structure = create_data_structure.__func__()

    @staticmethod
    def redefine_data_structure():
        """
        Refreshes DataStructure.data_structure as well as Structure.structure.
        Use this method after adding slides to the system.
        :return:
        """
        print("doing the job!")
        HciDataStructure.data_structure = HciDataStructure.create_data_structure()
        HciStructure.redefine_structure()
