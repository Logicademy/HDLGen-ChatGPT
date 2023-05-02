-- Description: mux41_32 4-to-1 Multiplexer, with 32-bit input data channels
-- Authors: Fearghal Morgan
-- Date: 4/2/2022
-- Change History: Original
-- 
-- sel(1:0)	  	2-bit data channel select (datapath control)	
-- muxIn3  		input byte-wide data channel 3
-- muxIn2  		input byte-wide data channel 2
-- muxIn1  		input byte-wide data channel 1
-- muxIn0  		input byte-wide data channel 0 
-- muxOut       output data channel 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

entity mux41_32 is
    Port ( sel 	      : in  STD_LOGIC_VECTOR(1 downto 0); 
           muxIn3     : in  STD_LOGIC_VECTOR(31 downto 0);   				
           muxIn2     : in  STD_LOGIC_VECTOR(31 downto 0);   				
           muxIn1     : in  STD_LOGIC_VECTOR(31 downto 0);   				
           muxIn0     : in  STD_LOGIC_VECTOR(31 downto 0);   				
           muxOut     : out STD_LOGIC_VECTOR(31 downto 0)
		  ); 
end mux41_32;

architecture combinational of mux41_32 is

begin

muxOut_i: process (sel, muxIn3, muxIn2, muxIn1, muxIn0)
begin
    muxOut <= muxIn0; -- default 
	if    sel =  "01" then muxOut <= muxIn1; 
	elsif sel =  "10" then muxOut <= muxIn2; 
	elsif sel =  "11" then muxOut <= muxIn3; 
	end if;
end process;

end combinational;