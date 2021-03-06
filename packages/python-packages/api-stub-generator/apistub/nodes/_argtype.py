import logging

# Special default values that should not be treated as string literal
SPECIAL_DEFAULT_VALUES = ["None", "..."]

# Lint warnings
TYPE_NOT_AVAILABLE = "Type is not available for {0}"

TYPE_NOT_REQUIRED = ["**kwargs", "self", "cls", "*", ]

class ArgType:
    """Represents Argument type
    :param str name: Name of the argument
    :param str argtype: Type of the argument. for e.g. str, int, BlobBlock
    :param str default: Default value for the argument, If any
    """

    def __init__(self, name, argtype=None, default=None, func_node = None):
        self.argname = name
        self.argtype = argtype
        self.default = default
        self.function_node = func_node


    def set_function_node(self, func_node):
        # Function node which is parent node can set it's refernce once docstring parser creates Argtype objects
        # This function node will be used to report any error found in arg while generating token.
        self.function_node = func_node


    def generate_tokens(self, apiview, function_id, add_line_marker):
        """Generates token for the node and it's children recursively and add it to apiview
        :param ~ApiVersion apiview: The ApiView
        :param str function_id: Module level Unique ID created for function 
        :param bool include_default: Optional flag to indicate to include/exclude default value in tokens
        """
        # Add arg name
        self.id = function_id
        if add_line_marker:
            self.id = "{0}.param({1}".format(function_id, self.argname)
            apiview.add_line_marker(self.id)

        apiview.add_text(self.id, self.argname)
        # add arg type
        if self.argtype:
            apiview.add_punctuation(":", False, True)
            apiview.add_type(self.argtype, self.id)
        elif self.argname not in (TYPE_NOT_REQUIRED):
            # Type is not available. Add lint error in review
            error_msg = TYPE_NOT_AVAILABLE.format(self.argname)
            apiview.add_diagnostic(error_msg, self.id)
            if self.function_node:
                self.function_node.add_error(error_msg)

        # add arg default value
        if self.default:
            apiview.add_punctuation("=", True, True)
            # Add string literal or numeric literal based on the content within default
            # Ideally this should be based on arg type. But type is not available for all args
            # We should refer to arg type instead of content when all args have type
            if self.default in SPECIAL_DEFAULT_VALUES or self.argtype != "str":
                apiview.add_literal(self.default)
            else:
                apiview.add_stringliteral(self.default)
