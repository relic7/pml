pml
===

PML Project
A PML document is a standard HTML document with one additional feature. Any text between the starting <pml> tag and the ending </pml> tag is interpreted as Python source code.
There can be multiple PML blocks in a PML file.
PML blocks will never nest.
The standard HTML should pass through the parser untouched.
The code within the PML tags should be executed with the python interpreter.
A technique should be implemented to write data to the output stream from within the PML. In other words the python code should be able to define the output that will replace the PML.
Variables and functions declared in one PML block should be available in subsequent PML blocks.
PML should be able to handle indentation dependent upon the first non-whitespace line of python code.
 
Example input:
 
<html>
<h1>Hello There</h1>
<p>
This is an example of a pml file
</p>
<pml>
    def f():
        return "<h2>Good Bye</h2>"
 
    pml = f()
</pml>
</html>
 
 
Example output:
 
<html>
<h1>Hello There</h1>
<p>
This is an example of a pml file
</p>
<h2>Good Bye</h2>
</html>
 
