# Project Settings

- The fields provide details on the current project 
	- 'Project Name' defines the HDLGen-Chat top level project folder, which may contain multiple 'Project Folders'
	- 'Project Folder' defines the name of the specific project folder, inside the 'Project Name' folder  
	- 'Project Environment' defines the fodler which contains the folder 'Package', which includes VHDL package file 'MainPackage.vhd' (used in VHDL models) 

- HDLGen-ChatGPT will remember the previously opened project

- Changing fields, and using the browser
	- Change the 'Project Name'  field and click the 'HDL Designer' TAB, to copy the entire project to a new area, with the defined 'Project Name'.
	- Change the 'Project Folder' and click the 'HDL Designer' TAB, to copy the entire project to a new area, with the defined 'Project Name', and within folder 'Project Folder'.
	- Change the 'Project Environment' and click the 'HDL Designer' TAB to save the 'Project Folder' and 'Project Name' within the environment folder. A new 'MainPackage.vhd' file may be created (and used), within folder 'Package'. It may be necessary to use the 'HDL Designer' TAB 'Sub-Components' menu to add componentents is your design isa hierarchical.
	
- Click the 'Close Project' button to close the project and return to the HDLGen-ChatGPT splash page 