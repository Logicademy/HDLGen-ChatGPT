/* 
Header Section
Component Name : threshold
Title          : Generate a 32-x32-bit threshold array from 32x32-byte source data array

Description
   Generate a 32-x32-bit threshold array from 
   32x32-byte source data array
   threshVal(7:0)
   Result bit is asserted if souce byte >= threshVal

Author(s)      : JP Byrne
Company        : University of Galway
Email          : j.byrne34@nuigalway.ie
Date           : 13/03/2023
*/

/* entity signal dictionary
clk	         clk signal
rst	         rst signal
ce	         threshold component enable. Assertion (h) activates the threshold register components
go	         Assertion (h) activates threshold finite state machine (FSM)
reg4x32_CSRA	4 x 32-bit register memory, control and status register A
reg4x32_CSRB	4 x 32-bit register memory, control and status register B
BRAM_dOut	  256-bit block RAM (BRAM) memory
active	     Asserted to highlight that FSM is active. Signal is a flag and is not used externally
wr	         Assertion (h) synchronously writes memory(add) = 
dataToMem(31:0)
add	        memory address
datToMem	memory write data
functBus	96-bit bus which can be connected to any threshold component signals, to be stored / viewed during threshold 
function execution
*/

/* internal signal dictionary
BRAMByte	BRAM_dOut(CSXAdd*8+7 downto CSXAdd*8)
threshVal	reg4x32_CSRA(31 downto 24)
NSYAdd	    Y address next state signal
            Y address current state signal, = NSYAdd on subsequent active clk edge, if ce is asserted
CSYAdd	    Y address next state signal
            Y address current state signal, = NSYAdd on subsequent active clk edge, if ce is asserted
NSXAdd	    X address next state signal
            X address current state signal, = NSXAdd on subsequent active clk edge, if ce is asserted
CSXAdd	    X address next state signal
            X address current state signal, = NSXAdd on subsequent active clk edge, if ce is asserted
NSthresholdVec	32-bit next state threshold vector signal. Asserted if BRAMByte(7:0) >= threshVal(7:0)
            32-bit current state threshold vector signal, = NSThreshVec on subsequent active clk edge, if ce is asserted
CSthresholdVec	32-bit next state threshold vector signal. Asserted if BRAMByte(7:0) >= threshVal(7:0)
            32-bit current state threshold vector signal, = NSThreshVec on subsequent active clk edge, if ce is asserted
NS	        Next state. Function of current state and input signals. Unregistered signal
            ??Current state. Increments synchronously on active clk edge. 
            Registered signal = NS on subsequent active clk edge, if ce is asserted
CS	        Next state. Function of current state and input signals. Unregistered signal
            Current state. Increments synchronously on active clk edge. 
            Registered signal = NS on subsequent active clk edge, if ce is asserted
*/ 

// module declaration
module threshold(
		clk,
		rst,
		ce,
		go,
		reg4x32_CSRA_128,
		reg4x32_CSRB_128,
		BRAM_dOut,
		
		active,
		wr,
		add,
		datToMem,
		functBus
	);

	// Port definitions
	input  clk;
	input  rst;
	input  ce;
	input  go;
	input  [127:0] reg4x32_CSRA_128;
	input  [127:0] reg4x32_CSRB_128;
	input  [255:0] BRAM_dOut;
	
output active;
	output wr;
	output [7:0] add;
	output [31:0] datToMem;
	output [95:0] functBus;

   // Internal signal declarations
   // Use localparam approach since it is more compact
   //   parameter idle = 2'b00;
   //   parameter chkBRAM_Byte_GT_thresholdValue = 2'b01;
   //   parameter wr_threshVec_to_reg32x32 = 2'b10;
   //   parameter write_status_to_reg4x32_CSRA0 = 2'b11;

   // Internal signal declarations

    // Declare states 
    localparam [1:0]
    idle = 0, 
    chkBRAM_Byte_GT_thresholdValue = 1, 
    wr_threshVec_to_reg32x32 = 2, 
    write_status_to_reg4x32_CSRA0 = 3;
    reg [1:0] NS;
    reg [1:0] CS;    

    wire [31:0] reg4x32_CSRA [3:0]; 
    wire [31:0] reg4x32_CSRB [3:0]; 
    wire [7:0]  BRAMByte;
    wire [7:0]  threshVal;
	
    reg [4:0]  NSYAdd;
    reg [4:0]  CSYAdd;
    reg [4:0]  NSXAdd;
    reg [4:0]  CSXAdd;
    reg [31:0] NSthresholdVec;
    reg [31:0] CSthresholdVec;

    reg active;
    reg wr;
    reg [7:0] add;
    reg [31:0] datToMem;

// FM TBD: add labels to assign statements
    assign {reg4x32_CSRA[3],reg4x32_CSRA[2],reg4x32_CSRA[1],reg4x32_CSRA[0]} = reg4x32_CSRA_128;
    assign BRAMByte = BRAM_dOut[CSXAdd]; 
    assign threshVal = reg4x32_CSRA[0][15:8]; // check indices 
    assign functBus = {reg4x32_CSRA[2], reg4x32_CSRB[1], reg4x32_CSRA[0]}; // Complete the concurrent statement if required 
    
    // stateReg 
    always @(posedge clk or posedge rst) 
     begin : stateReg
    	// Complete the process if required
    	if ( rst ) 
		 begin
    		CS <= idle;
    		CSYAdd <= 5'b0;
    		CSXAdd <= 5'b0;
    		CSthresholdVec <= 32'b0;
    	 end
		else
		 begin
		    if (ce)
    	 	 begin 
    		  CS <= NS;
    		  CSYAdd <= NSYAdd;
    		  CSXAdd <= NSXAdd;
    		  CSthresholdVec <= NSthresholdVec;
    		 end
	     end 
     end
    
    // NSAndOPDecode 
	always @(go or BRAMByte or threshVal or CS or CSYAdd or CSXAdd or CSthresholdVec )
   	  begin : NSAndOPDecode
        // Complete the process if required
    	case ( CS )
    		idle:
    			begin
				  // assign other output signal states
    		      active <= 1'b0;
                  if (go) 
                   NS <= chkBRAM_Byte_GT_thresholdValue;
    			end
    		 chkBRAM_Byte_GT_thresholdValue:
    			begin 
    		      NSYAdd <= CSYAdd + 1; 
    		      NSXAdd <= CSXAdd + 1; 
    		      if (BRAMByte == threshVal) 
    		       begin 
    		        NSthresholdVec <= CSthresholdVec + 1;                 
                    NS <= wr_threshVec_to_reg32x32;
                   end 
    			end
    		 wr_threshVec_to_reg32x32:
    			begin
    		      wr <= 1'b1; 
    		      add <= {3'b0, CSYAdd};
                  datToMem <= CSthresholdVec;
                  NS <= write_status_to_reg4x32_CSRA0;
    			end
    		 write_status_to_reg4x32_CSRA0:
    			begin
    		      wr <= 1'b1; 
    		      add <= {3'b0, CSYAdd};
                  datToMem <= {reg4x32_CSRA[0][31:1], 1'b1};
                  NS <= idle;
    			end
    		default:
    			begin
				  // don't included the // default label in the generated verilog file
    		      active <= 1'b1;
    		      wr <= 1'b0; 
    		      add <= 8'b0;
    		      datToMem <= 32'b0; 
    		      NS <= CS; 
    		      NSYAdd <= CSYAdd; 
    		      NSXAdd <= CSXAdd; 
    		      NSthresholdVec <= CSthresholdVec;                 
    			end
    	endcase
      end

endmodule