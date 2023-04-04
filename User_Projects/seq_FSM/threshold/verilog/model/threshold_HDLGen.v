// Header Section
// Component Name : threshold
// Title          : Generate a 32-x32-bit threshold array from 32x32-byte source (BRAM) data array

// Description
// Generate a 32-x32-bit threshold array from 
// - 32x32-byte source (BRAM) data array
// - threshVal(7:0)
// 
// Result bit is asserted if source byte >= threshVal

// Author(s)      : Fearghal Morgan
// Company        : University of Galway
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 03/04/2023

// entity signal dictionary
// ce	threshold component enable. Assertion (h) activates the 
// threshold register components.
// go	Assertion (h) activates threshold finite state machine (FSM)
// reg4x32_CSRA	4 x 32-bit register memory, control and status register A
// reg4x32_CSRB	4 x 32-bit register memory, control and status register B
// BRAM_dOut	256-bit block RAM (BRAM) memory
// active	Asserted to highlight that FSM is active. Signal is a flag and 
// is not used externally.
// wr	Assertion (h) synchronously writes memory(add) = 
// dataToMem(31:0)
// add	memory address
// datToMem	memory write data
// functBus	96-bit bus which can be connected to any threshold 
// component signals, to be stored / viewed during threshold 
// function execution
// clk	clk signal
// rst	rst signal

// internal signal dictionary
// NSYAdd	Y address std_logic_vector state signals
// CSXAdd	X address std_logic_vector current state signal
// CSYAdd	Y address std_logic_vector current state signal
// CSThreshVec	thresholdVec std_logic_vector current state signals
// NSThreshVec	thresholdVec std_logic_vector next state signal
// threshVal	threshVal(7:0) = reg4x32_CSRA(31:24)
// NSCS	Finite State Machine (FSM) next state and current state
// CSCS	Finite State Machine (FSM) next state and current state
// BRAMByte	BRAM_dOut(CSXAdd*8+7 : CSXAdd*8)
// NSXAdd	X address std_logic_vector state signals



// module declaration
module threshold(
		ce,
		go,
		reg4x32_CSRA,
		reg4x32_CSRB,
		BRAM_dOut,
		active,
		wr,
		add,
		datToMem,
		functBus,
		clk,
		rst
	);

	// Port definitions
	input  ce;
	input  go;
	input reg4x32_Array reg4x32_CSRA;
	input reg4x32_Array reg4x32_CSRB;
	input [255:0] BRAM_dOut;
	output  active;
	output  wr;
	output [7:0] add;
	output [31:0] datToMem;
	output [95:0] functBus;
	input  clk;
	input  rst;

    reg  active;
    reg  wr;
    wire [7:0] add;
    reg [31:0] datToMem;
    reg [95:0] functBus;

    // Internal signal declarations
    parameter idle = 2'b00;
    parameter chkBRAM_Byte_GT_thresholdValue = 2'b01;
    parameter wr_threshVec_to_reg32x32 = 2'b10;
    parameter write_status_to_reg4x32_CSRA0 = 2'b11;
    reg [4:0] NSYAdd;
    reg [4:0] CSXAdd;
    reg [4:0] CSYAdd;
    reg [4:0] CSThreshVec;
    reg [31:0] NSThreshVec;
    reg [31:0] threshVal;
    reg  NSCS;
    reg  CSCS;
    wire [7:0] BRAMByte;
    reg [7:0] NSXAdd;

    always @(go or reg4x32_CSRA or reg4x32_CSRB or CSYAdd or CSXAdd or BRAMByte or CS  or threshVal )
    begin : NSAndOPDecode_p
    	// Complete the process if required
    	active <= ; // default assignment
    	wr <= 1'b0; // default assignment
    	add <= all zeros; // default assignment
    	datToMem <= all zeros; // default assignment
    	NSYAdd <= CSYAdd; // default assignment
    	NSXAdd <= CSXAdd; // default assignment
    	NS  <= CS ; // default assignment
    end

    always @(posedge clk or posedge rst )
    begin : stateReg_p
    	// Complete the process if required	
    	if ( rst )
    		begin
    		CS  <= Idle;

    		CSYAdd <= all zeros;

    		CSXAdd <= all zeros;

    		CSthreshVec <= all zeros;
    		end
    	else
    		begin
    		CS  <= NS ;
    		CSYAdd <= NSYAdd;
    		CSXAdd <= NSXAdd;
    		CSthreshVec <= NSthreshVec;
    		end
    end

    assign add = all zeros; // Complete the concurrent statement if required
    assign BRAMByte = all zeros; // Complete the concurrent statement if required

endmodule

