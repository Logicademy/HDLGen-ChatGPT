-- Header Section
-- Component Name : AND2_1
-- Title          : 2-input AND logic model, 1-bit data
-- Description
-- 
-- Author(s)      : Fearghal Morgan
-- Company        : University of Galway
-- Email          : fearghal.morgan@universityofgalway.ie
-- Date           : 13/01/2023

-- entity signal dictionary
--  AND2In1  input, 1-bit data
--  AND2In0  input, 1-bit data
--  AND2Out  output, 1-bit data 

-- internal signal dictionary
-- None

-- library declarations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- entity declaration
entity ANDTest is 
Port(
	andIn1 : in std_logic;
	andIn0 : in std_logic;
	andOut : out std_logic
);
end entity ANDTest;

architecture comb of ANDTest is
-- Internal signal declarations

-- Component declarations

begin

andOut_c: andOut <= andIn1 and andIn0;

end comb;