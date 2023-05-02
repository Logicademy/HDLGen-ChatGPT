-- Header Section
-- Component Name : mux21_4
-- Title          : mux21_4 title

-- Description
-- mux21_4 description

-- Author(s)      : Fearghal Morgan
-- Company        : UG
-- Email          : fearghal.morgan@universityofgalway.ie
-- Date           : 02/04/2023

-- entity signal dictionary
-- mux21_4_In1	mux21_4_In1 description
-- mux21_4_In0	mux21_4_In0 description
-- sel	sel description
-- mux21_4_Out	mux21_4_Out description

-- internal signal dictionary
-- None

-- library declarations
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.MainPackage.all;


-- entity declaration
entity mux21_4 is 
Port(
	mux21_4_In1 : in std_logic_vector(3 downto 0);
	mux21_4_In0 : in std_logic_vector(3 downto 0);
	sel : in std_logic;
	mux21_4_Out : out std_logic_vector(3 downto 0)
);
end entity mux21_4;

architecture Combinational of mux21_4 is
-- Internal signal declarations
-- None

begin

mux21_4_p: process(mux21_4_In1,mux21_4_In0,sel)
begin
	mux21_4_Out <= mux21_4_In0;-- default
	if sel = '1' then
	  mux21_4_Out <= mux21_4_In1; 
	end if;
	
end process;

end Combinational;