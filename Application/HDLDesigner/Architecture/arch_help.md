# Architecture 

This menu enables the creation and editing of processes, concurrent statements and component instantiations

- New process
	- Process name
	- suffix (_p default)
	- Add non-default logic 
		- Examples
			if RWr = 1
				if rd > 0
					NSArray(rd) = WBDat
				end if
			end if

			Use nested, indented if-elsif-else-end if and case-end case stateements

	- sensitivity list: tick all signals which apply
		synchronous (clocked): clk and/or rst are automatically validated as the sensitivity list 
	- Select 
		- output signal 
			- select signal 
			- default values
				- select 
					signal name or	
					'zero'
					custom value 				
						- enter custom default value
		- Click OK to complete
		
		
- New concurrent statement
	- concurrent statement name 
	- default suffix is _c
	- assign signal 
		- select signal to be assigned or 
		- 'zero'
		- click 'custom value' to enter custom value, e.g, equation in the custom value field
	- Click OK to complete

- New (component) instance
	- instance name	
	- suffix (_i defaul)
	- component list (accesses the components listed in the sub-components menu
		- assign input or internal signal name to the component port signals
	- Click OK to complete
	
- The existing processes, concurrent statements and component instances are listed and can be edited or deleted
