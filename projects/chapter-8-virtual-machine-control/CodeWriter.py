"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self._output_stream = output_stream
        self._asm_code = ""
        self._label_counter = 0
        segment_initialization = "// initialization\n"
        segment_initialization += "@256\n"
        segment_initialization += "D=A\n"
        segment_initialization += "@SP\n"
        segment_initialization += "M=D\n"
        segment_initialization += "@LCL\n"
        segment_initialization += "@ARG\n"
        segment_initialization += "@THIS\n"
        segment_initialization += "@THAT\n"
        segment_initialization += "@TEMP\n"
        self._output_stream.write(segment_initialization)


    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        if command == "add":
            write = "// add\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "M=D+M\n"
        elif command == "sub":
            write = "// sub\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "M=M-D\n"
        elif command == "neg":
            write = "// neg\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "M=-M\n"
        elif command == "eq":
            write = "// eq\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "D=D-M\n"
            write += f"@IS_EQUAL{self._label_counter}\n"
            write += "D;JEQ\n"
            write += "D=-1\n"
            write += f"(IS_EQUAL{self._label_counter})\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "M=!D\n"
            self._label_counter = self._label_counter + 1
        elif command == "gt":
            write = "// gt\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "D=D-M\n"
            write += f"@IS_GREATER{self._label_counter}\n"
            write += "D;JLT\n"
            write += "D=-1\n"
            write += f"@ASSIGN_BOOLEAN{self._label_counter}\n"
            write += "D;JMP\n"
            write += f"(IS_GREATER{self._label_counter})\n"
            write += "D=0\n"
            write += f"(ASSIGN_BOOLEAN{self._label_counter})\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "M=!D\n"
            self._label_counter = self._label_counter + 1
        elif command == "lt":
            write = "// lt\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "D=D-M\n"
            write += f"@IS_LESS{self._label_counter}\n"
            write += "D;JGT\n"
            write += "D=0\n"
            write += f"@ASSIGN_BOOLEAN{self._label_counter}\n"
            write += "D;JMP\n"
            write += f"(IS_LESS{self._label_counter})\n"
            write += "D=-1\n"
            write += f"(ASSIGN_BOOLEAN{self._label_counter})\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "M=D\n"
            self._label_counter = self._label_counter + 1
        elif command == "and":
            write = "// and\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "M=D&M\n"
        elif command == "or":
            write = "// or\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "D=M\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M-1\n"
            write += "M=D|M\n"
        elif command == "not":
            write = "// not\n"
            write += "@SP\n"
            write += "A=M-1\n"
            write += "M=!M\n"
        self._output_stream.write(write)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        _segment = "constant"
        if segment == "local":
            _segment = "LCL"
        elif segment == "argument":
            _segment = "ARG"
        elif segment == "this":
            _segment = "THIS"
        elif segment == "pointer":
            if index == "0":
                _segment = "PTR_THIS"
            elif index == "1":
                _segment = "PTR_THAT"
            else:
                print("error occured attempting to decode pointer")
        elif segment == "that":
            _segment = "THAT"
        elif segment == "temp":
            _segment = "TEMP"
        elif segment == "static":
            _segment = "STATIC"

        if command == "C_PUSH":
            write = f"// push {segment} {index}\n"
            if _segment == "constant":
                write += f"@{index}\n"
                write += "D=A\n"
            elif _segment == "TEMP":
                write += "@5\n"
                write += "D=A\n"
                write += f"@{index}\n"
                write += "A=D+A\n"
                write += "D=M\n"
            elif _segment == "PTR_THIS":
                write += "@THIS\n"
                write += "D=M\n"
            elif _segment == "PTR_THAT":
                write += "@THAT\n"
                write += "D=M\n"
            elif _segment == "STATIC":
                write += f"@{index}\n"
                write += "D=A\n"
                write += "@16\n"
                write += "A=D+A\n"
                write += "D=M\n"
            else:
                write += f"@{index}\n"
                write += "D=A\n"
                write += f"@{_segment}\n"
                write += "A=M+D\n"
                write += "D=M\n"
            write += "@SP\n"
            write += "A=M\n"
            write += "M=D\n"
            write += "@SP\n"
            write += "M=M+1\n"
        elif command == "C_POP":
            write = f"// pop {segment} {index}\n"
            write += f"@{index}\n"
            write += "D=A\n"
            write += f"@{_segment}\n"
            if _segment == "TEMP":
                write += f"@5\n"
                write += "D=A+D\n"
            elif _segment == "PTR_THIS":
                write += "@THIS\n"
                write += "D=A\n"
            elif _segment == "PTR_THAT":
                write += "@THAT\n"
                write += "D=A\n"
            elif _segment == "STATIC":
                write += f"@{index}\n"
                write += "D=A\n"
                write += "@16\n"
                write += "D=D+A\n"
            else:
                write += "D=M+D\n"
            write += "@R13\n"
            write += "M=D\n"
            write += "@SP\n"
            write += "M=M-1\n"
            write += "A=M\n"
            write += "D=M\n"
            write += "@R13\n"
            write += "A=M\n"
            write += "M=D\n"

        self._output_stream.write(write)


    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        self.write_line(f"({label})")


    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.write_line(f"@{label}")
        self.write_line("D;JMP")


    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        self.write_line("// goto-if")
        self.write_line("@SP")
        self.write_line("M=M-1")
        self.write_line("A=M")
        self.write_line("D=M")
        self.write_line(f"@{label}")
        self.write_line("D;JNE")


    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.write_line("@SP")
        self.write_line("M=M+1")
        self.write_line("A=M-1")
        self.write_line("M=0")

    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.write_line("// return")
        self.write_line("@LCL")
        self.write_line("D=M")
        self.write_line("@TEMP")
        self.write_line("M=D")
        self.write_line("@5")
        self.write_line("D=A")
        self.write_line("@TEMP")
        self.write_line("A=M-D")
        self.write_line("D=M")
        self.write_line("@return_address")
        self.write_line("M=D")
        self.write_line("@SP")
        self.write_line("M=M-1")
        self.write_line("A=M")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("A=M")
        self.write_line("M=D")
        # SP = ARG+1
        self.write_line("@ARG")
        self.write_line("D=M")
        self.write_line("@1")
        self.write_line("D=D+A")
        self.write_line("@SP")
        self.write_line("M=D")
        # THAT = *(frame-1)
        self.write_line("@1")
        self.write_line("D=A")
        self.write_line("@TEMP")
        self.write_line("A=M-D")
        self.write_line("D=M")
        self.write_line("@THAT")
        self.write_line("M=D")
        # THIS = *(frame-2)
        self.write_line("@2")
        self.write_line("D=A")
        self.write_line("@TEMP")
        self.write_line("A=M-D")
        self.write_line("D=M")
        self.write_line("@THIS")
        self.write_line("M=D")
        self.write_line("@3")
        self.write_line("D=A")
        self.write_line("@TEMP")
        self.write_line("A=M-D")
        self.write_line("D=M")
        self.write_line("@ARG")
        self.write_line("M=D")
        self.write_line("@4")
        self.write_line("D=A")
        self.write_line("@TEMP")
        self.write_line("A=M-D")
        self.write_line("D=M")
        self.write_line("@LCL")
        self.write_line("M=D")
        self.write_line("@return_address")
        self.write_line("A=M")
        self.write_line("D;JMP")


    def write_line(self, line: str) -> None:
        self._asm_code = line + "\n"
        self._output_stream.write(self._asm_code)


    def finish(self) -> None:
        write = "// finisg assembly code with infinite loop\n"
        write += "(END)\n"
        write += "@END\n"
        write += "D;JMP\n"
        self._output_stream.write(write)

