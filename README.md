# Food QA system language technology collaboration

Repository used for collaborating on University of Groningen Language Technology course final project.

NOTE 1
always run the script from this directory, with the command
python3 qa_system.py

NOTE 2
in qa_system.py, I enabled the debug_modus, so you see what is going on in the functions.
Note that the debug modus in question() causes that the program works. 
Since this function is empty, I temporarely made the entity 'kfc' and the property 'founded by'

NOTE 3
I only made a 'base case' based on WikidataAPI. AnchorText should still be implemented

NOTE 4
The function formulate_answer() only formulates an answer based on the 'what is X of Y' and 'list' cases. The others have to be implemented

IMPORTANT NOTE
The anchorText in the /data/ folder is NOT real. Since gitHub doesn't accept files +25MB
