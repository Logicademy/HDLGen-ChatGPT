// Header Section
// Component Name : ADD2
// Title          : 2-bit binary adder

// Description
// 2-bit binary adder
// 
// -- IEEE.numeric_std library + function used in this model
// which converts an 
// -- unsigned vector to type std_logic_vector, the type of the signal 
// sum

// Author(s)      : Fearghal Morgan
// Company        : University of Galway
// Email          : fearghal.morgan@universityofgalway.ie
// Date           : 29/03/2023

// entity signal dictionary
// addIn1	2-bit input
// addIn0	2-bit input
// sum	2-bit output

// internal signal dictionary
// None



// module declaration
module ADD2(
		addIn1,
		addIn0,
		sum
	);

	// Port definitions
	input [1:0] addIn1;
	input [1:0] addIn0;
	output [1:0] sum;

    wire [1:0] sum;

    // Internal signal declarations
    // None

    assign sum = addIn1; // Complete the concurrent statement if required

endmodule

