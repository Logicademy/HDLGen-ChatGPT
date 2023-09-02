# ChatGPT 

- Selection of VHDL or Verilog generation is performed in the HDL Designer menu

- This menu 

	- loads and previews the default ChatGPT prompt headers
		- Model 
		- enables editing of the ChatGPT prompt headers
	
	- Generates and previews  HDL templates (and backups the previous version) for
		- HDL model
		- HDL testbench
		
	- Assembles, previews, copies the ChatGPT prompt, for (and backups the previous prompt)
		- completion of HDL model
			- ChatGPT prompt header elements
				- ChatGPT prompt header for HDL model template completion
				- HDLGen-ChatGPT-generated HDL model tempalte 				
		- generation of HDL testbench stim_p stimulus and signal checking
			- 	ChatGPT prompt header elements
				- ChatGPT prompt header for HDL testbench stim_p generation 
				- testbench signal declarations
				- test plan (fromatted)
			
	- Accesses 
		- folder
		- AMD simulator log files
		- backups and clears backup files) 
		
		
HDLGen-ChatGPT allows users to modify and test the ChatGPT prompt headers. 
This facilitates handling of any issue uncovered during HDL generation for a particular design, 
or accommodating any future changes which may occur in ChatGPT functionality, affecting generated HDL code output. 

The Edit ChatGPT Prompt Header menu opens an editor, displaying and facilitating editing of the selected 
ChatGPT prompt and descriptive comment (with ~ comment prefix).
ChatGPT prompts in the HDL Designer > Generate menu, are used for HDL model and HDL testbench HDL generation. 
The user selects VHDL or Verilog in the Project Manager TAB.

An issue can be detected in a generated HDL process or concurrent statement, on review of ChatGPT code or 
by a warning or error flagged in the EDA tool. The ChatGPT prompt header can include comments using (~) prefix, 
with a ChatGPT prompt instruction to ignore these comments. 

Prompt header comments can be used for description of the reason for the prompt, though also to filter 
a ChatGPT prompt to output an individual HDL section, e.g, process or concurrent statement. 
The user can subsequently submit focused ChatGPT prompts to query the generated code segment, and request 
alternative ChatGPT output. The refined HDL output segment can be pasted into the EDA tool, for further checking 
and processing. This incremental HDL generation approach can be very effective. Backups of all ChatGPT prompts 
are automatically generated and can be accessed through the HDLGen-ChatGPT generate menu. Note that the incremental 
approach diverges from the use of a single crafted ChatGPT prompt and requires the recording of subsequent prompts 
by the user, since re-running the original ChatGPT prompt over-writes the latest generated HDL.

An issue can be detected in a generated HDL process or concurrent statement, on review of ChatGPT code 
or by a warning or error flagged in the EDA tool. The ChatGPT prompt header can include comments using (~) prefix, 
with a ChatGPT prompt instruction to ignore these comments. Prompt header comments can be used for description of 
the reason for the prompt, though also to filter a ChatGPT prompt to output an individual HDL section, e.g, process 
or concurrent statement. The user can subsequently submit focused ChatGPT prompts to query the generated code segment, 
and request alternative ChatGPT output. The refined HDL output segment can be pasted into the EDA tool, for further 
checking and processing. This incremental HDL generation approach can be very effective. Backups of all ChatGPT 
prompts are automatically generated and can be accessed through the HDLGen-ChatGPT generate menu. Note that the 
incremental approach diverges from the use of a single crafted ChatGPT prompt and requires the recording of subsequent 
prompts by the user, since re-running the original ChatGPT prompt over-writes the latest generated HDL.


	