-- Description: selDSPOutSigs
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 7/10/2022

-- Input signals
--  sel			(4:0) selects up to 32 data paths 
--
-- Up to 32 combination of the following signals
--  datToMem(31:0)
--  add(7:0)
--  wr
--  functBus(95:0)
--
-- Generates
--   DSP_datToMem(31:0)
--   DSP_memAdd(7:0)
--   DSP_memWr 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity selDSPOutSigs is
    Port ( sel      : in std_logic_vector(4 downto 0); 
		   datToMem : in array32x32;
           add      : in array32x8;
           wr       : in std_logic_vector(31 downto 0);
           functBus : in array32x96;
	
           DSP_datToMem : out std_logic_vector(31 downto 0);              
           DSP_memAdd   : out std_logic_vector(7 downto 0);                      
           DSP_memWr    : out std_logic;
           DSP_functBus : out std_logic_vector(95 downto 0)
		  );
end selDSPOutSigs;
						 
architecture comb of selDSPOutSigs is
begin

DSP_datToMem <= datToMem( to_integer(unsigned(sel)) );
DSP_memAdd   <= add( to_integer(unsigned(sel)) );
DSP_memWr    <= wr( to_integer(unsigned(sel)) );
DSP_functBus <= functBus( to_integer(unsigned(sel)) );

end comb;