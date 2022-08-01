-- Header Section
-- Component Name : ANDTest
-- Title          : AND gate model
-- Description    : aadfsdaaaaaaaaaaaaaaaaa
 	--agagg
 	--agggas
 	--afhafddjj
 	--kkkk
-- Author(s)      : FM
-- Company        : NUIG
-- Email          : f@n.ie
-- Date           : 23/07/2022


-- Library Section
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- Entity Section
entity ANDTest is 
Port(
	andIn1 : in std_logic;
	andIn0 : in std_logic;
	andOut : out std_logic
);
end entity ANDTest;

architecture comb of ANDTest is

-- Internal Signals


begin

andOut_c: andOut <= andIn1 and andIn0;

end comb;