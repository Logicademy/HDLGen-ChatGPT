/* 
Header Section
Component Name : threshold
Title          : Generate a 32-x32-bit threshold array from 32x32-byte source data array

Description
   Generate a 32-x32-bit threshold array from 
   32x32-byte source (BRAM) data array
   threshVal(7:0)
   Result bit is asserted if source (BRAM) byte >= threshVal

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
threshVal	reg4x32_CSRA(0)(31 downto 24) // check this FM
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
	
    reg active;
    reg wr;
    reg [7:0] add;
    reg [31:0] datToMem;

    reg [1:0] NS;
    reg [1:0] CS;    
    reg [4:0]  NSYAdd;
    reg [4:0]  CSYAdd;
    reg [4:0]  NSXAdd;
    reg [4:0]  CSXAdd;
    reg [31:0] NSThreshVec;
    reg [31:0] CSThreshVec;
    wire [7:0]  BRAMByte;
    wire [7:0]  threshVal;

// handling arrays: create internal array signal
    wire [31:0] reg4x32_CSRA [3:0]; 
    wire [31:0] reg4x32_CSRB [3:0]; 
 
// FM automate generation of array from concatentation port vector signal
// assign {reg4x32_CSRA[3],reg4x32_CSRA[2],reg4x32_CSRA[1],reg4x32_CSRA[0]} = reg4x32_CSRA_128;
    assign reg4x32_CSRA[3] = reg4x32_CSRA_128[127:96];
    assign reg4x32_CSRA[2] = reg4x32_CSRA_128[95:64];
    assign reg4x32_CSRA[1] = reg4x32_CSRA_128[63:32];
    assign reg4x32_CSRA[0] = reg4x32_CSRA_128[31:0];
// assign {reg4x32_CSRB[3],reg4x32_CSRB[2],reg4x32_CSRB[1],reg4x32_CSRB[0]} = reg4x32_CSRB_128;
    assign reg4x32_CSRB[3] = reg4x32_CSRB_128[127:96];
    assign reg4x32_CSRB[2] = reg4x32_CSRB_128[95:64];
    assign reg4x32_CSRB[1] = reg4x32_CSRB_128[63:32];
    assign reg4x32_CSRB[0] = reg4x32_CSRB_128[31:0];
 
// Assign internal signals
    assign BRAMByte = BRAM_dOut[CSXAdd*8 +:8];// take 8 bit slice, starting at bit CSXAdd*8
    assign threshVal = reg4x32_CSRA[0][15:8]; // check indices 
	
// Assign output signals
    assign functBus = 128'h0;
    
    // stateReg 
    always @(posedge clk or posedge rst) 
     begin : stateReg
    	// Complete the process if required
    	if ( rst ) 
		 begin
    		CS <= idle;
    		CSYAdd <= 5'b0;
    		CSXAdd <= 5'b0;
    		CSThreshVec <= 32'b0;
    	 end
		else
		 begin
		    if (ce)
    	 	 begin 
    		  CS <= NS;
    		  CSYAdd <= NSYAdd;
    		  CSXAdd <= NSXAdd;
    		  CSThreshVec <= NSThreshVec;
    		 end
	     end 
     end
    
    // NSAndOPDecode 
    // Complete the process if required
	always @(CS or go or reg4x32_CSRA[0] or reg4x32_CSRB[0] or CSYAdd or CSXAdd or CSThreshVec or threshVal or BRAMByte)
   	  begin : NSAndOPDecode
        NS     <= CS;   // default
        active <= 1'b1; // default asserted
        NSYAdd <= CSYAdd;
        NSXAdd <= CSXAdd;
        NSThreshVec <= CSThreshVec;
        wr <= 1'b0; 
        add <= {3'b010, CSYAdd}; // address 32 x 256-bit BRAM
	    datToMem <= CSThreshVec;

    	case ( CS )
    		idle:
    			begin
     		      NSYAdd <= 0; 
    		      NSXAdd <= 0;
    		      NSThreshVec <= 0; 
				  // assign other output signal states
                  if (go) 
                    begin
                      NS <= chkBRAM_Byte_GT_thresholdValue;
					  add <= {3'b010, CSYAdd}; // address 32 x 256-bit BRAM
                    end
				  else
				    begin
	      		      active <= 1'b0;
					end
    			end

    		 chkBRAM_Byte_GT_thresholdValue:
    			begin 
				  add <= {3'b010, CSYAdd}; // address 32 x 256-bit BRAM
			      if (BRAMByte > threshVal)      
			        begin
			          NSThreshVec[CSXAdd] <= 1'b1; // set single bit of vector
			        end 
			      NSXAdd <= CSXAdd + 1;   // increment XAdd counter
				  if (NSXAdd == 31)
				    begin
				      NS <= wr_threshVec_to_reg32x32; // final threshVec value is ready in wr_threshVec_to_reg32x32 state
				    end 
				end

    		 wr_threshVec_to_reg32x32:
    			begin
    		      wr <= 1'b1; 
                  add <= {3'b001, CSYAdd}; // resultMem address
                  datToMem <= CSThreshVec;
                  NS <= write_status_to_reg4x32_CSRA0;
	              NSThreshVec <= 0;
			      NSYAdd <= CSYAdd + 1;        // increment YAdd counter
		          NS <= chkBRAM_Byte_GT_thresholdValue; // loop, to process next BRAM word
	   		      if (NSYAdd == 31) 
				    NS <= write_status_to_reg4x32_CSRA0;    // final threshVec value is ready in wr_threshVec_to_reg32x32 state
    			 end

    		 write_status_to_reg4x32_CSRA0:
    			begin
    		      wr <= 1'b1; 
				  add <= 8'b0; // address CSRA[0]
                  datToMem <= {reg4x32_CSRA[0][31:2], 2'b10};
                  NS <= idle;
    			end
								
    		default:
    			begin
    			end
    	endcase
      end

endmodule