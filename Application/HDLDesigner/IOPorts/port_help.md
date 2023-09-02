# Port 

- This menu enables the creation and editing of component port signals, with 
	- port direction: input or output 
	- port signal type

- The menu display name, mode, type and size for added port signals

- If select 'combinational'
	- add signal
		- signal name
		- mode: input or output
		- type: single bit, bus, array
		- size (width): enter value in the field
		- signal description: capture the signal dictionary information fromt the design specification
		- Click OK to complete

- If select 'RTL'
	- Setup clk/rst menu appears. Click to open menu.
		- L-H low to high active clk edge
		- H-L high to low active clk edge
		- rst
			- No if component does not include a rst input 
			- Yes
				- rst type	
					- Asynch: asynchronous rst
					- Synch:  synchronous rst					
				- active rst level 
					- 0, asserted low
					- 1, asserted high
		- Click OK to complete
		
- The existing port signals are listed and can be edited or deleted.