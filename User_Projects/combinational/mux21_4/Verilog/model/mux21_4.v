// Header Section
// Component Name : mux21_4
// Title          : mux21_4 title

// Description
// mux21_4 description

// Author(s)      : Fearghal Morgan
// Company        : UG
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 27/03/2023

// entity signal dictionary
// mux21_4_In1	mux21_4_In1 description
// mux21_4_In0	mux21_4_In0 description
// sel	sel description
// mux21_4_Out	mux21_4_Out description

// internal signal dictionary
// None



// module declaration
module mux21_4(
		mux21_4_In1,
		mux21_4_In0,
		sel,
		mux21_4_Out
	);

	// Port definitions
	input [3:0] mux21_4_In1;
	input [3:0] mux21_4_In0;
	input  sel;
	output [3:0] mux21_4_Out;

    reg [3:0] mux21_4_Out;

    // Internal signal declarations
    // None

    always @(mux21_4_In1 or mux21_4_In0 or sel )
    begin : mux21_4_p
    	// Complete the process if required
    	mux21_4_Out <= mux21_4_In0; // default assignment
    	if (sel) 
      	  begin 
      	     mux21_4_Out <= mux21_4_In1;
      	  end 
    end


endmodule

