-- Description: selDSPOrHostCtrl
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 7/1/2021

-- Description
-- select memory master (host or DSP function), and generates signals wr, add, datToMem 

-- Signal dictionary

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity selDSPOrHostCtrl is
    Port ( DSPMaster           : in  std_logic;

	       host_memWr        : in  std_logic;
	       host_memAdd       : in  std_logic_vector(10 downto 0);
		   host_datToMem     : in  std_logic_vector(255 downto 0);
	       
	       DSP_memWr         : in  std_logic;
	       DSP_memAdd        : in  std_logic_vector(7 downto 0);
		   DSP_datToMem      : in  std_logic_vector(31 downto 0);

	       memWr             : out std_logic;
	       memAdd            : out std_logic_vector(10 downto 0);
		   datToMem          : out std_logic_vector(255 downto 0)
           );
end selDSPOrHostCtrl;
						 
architecture comb of selDSPOrHostCtrl is

begin

process (DSPMaster, 
         host_memWr, host_memAdd, host_datToMem,
         DSP_memWr,  DSP_memAdd,  DSP_datToMem)
begin
	memWr    <= host_memWr; -- defaults
	memAdd   <= host_memAdd; 
	datToMem <= host_datToMem;

	if DSPMaster = '1' then
		memWr                   <= DSP_memWr;
		memAdd                  <= "000" & DSP_memAdd; 
		datToMem(255 downto 32) <= (others => '0');
		datToMem( 31 downto  0) <= DSP_datToMem;
	end if;
end process;

end comb;