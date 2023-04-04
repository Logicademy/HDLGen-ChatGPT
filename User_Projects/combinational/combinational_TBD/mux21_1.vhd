--  Model name		mux21_1 
--  Description		2-to-1 multiplexer datapath selector 
--  Author(s)		Fearghal Morgan
--  Company			National University of Ireland, Galway 
--  Date			14th July 2012
--  Change History 	Initial version
--
-- Signal dictionary
--  sel 	   data path select input, '0'/'1' passes muxIn0/1 data to muxOut
--  muxIn1     input data path 1
--  muxIn0     input data path 0
--  muxOut     output data

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity mux21_1 is
    Port ( sel 	  : in  STD_LOGIC;  
           muxIn1 : in  STD_LOGIC;  
           muxIn0 : in  STD_LOGIC;  
           muxOut : out STD_LOGIC   
          );
end mux21_1;

architecture combinational of mux21_1 is
begin

muxOut_i: process (sel, muxIn1, muxIn0)
begin	
	muxOut <= muxIn0; -- default
	if sel = '1' then 
		muxOut <= muxIn1;
	end if;
end process;

end combinational;