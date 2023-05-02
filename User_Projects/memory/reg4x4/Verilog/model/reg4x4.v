// Header Section
// Component Name : reg4x4
// Title          : reg4x4 title

// Description
// reg4x4 description

// Author(s)      : Fearghal Morgan
// Company        : UG
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 27/03/2023

// entity signal dictionary
// clk	clk signal
// rst	rst signal
// ce	ce description
// we	we description
// add	add description
// dIn	dIn description
// dOut	dOut array description

// internal signal dictionary
// NS	Current and next state signal description
// CS	Current and next state signal description



// module declaration
module reg4x4(
		clk,
		rst,
		ce,
		we,
		add,
		dIn,
		dOut
	);

	// Port definitions
	input  clk;
	input  rst;
	input  ce;
	input  we;
	input [1:0] add;
	input [3:0] dIn;
	output reg4x4_Array dOut;

    reg reg4x4_Array dOut;

    // Internal signal declarations
    reg [3:0] NS;
    reg [3:0] CS;

    always @(posedge clk or posedge rst )
    begin : stateReg_p
    	// Complete the process if required	
    	if ( rst )
    		begin
    		CS <= 4'b0;
    		end
    	else
    		begin
    		CS <= NS;
    		end
    end

    always @(ce or we or add or dIn or CS )
    begin : NSDecode_p
    	// Complete the process if required
    	NS <= ; // default assignment
    end

    assign dOut = CS; // Complete the concurrent statement if required

endmodule

