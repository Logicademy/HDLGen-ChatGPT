-- Description: decodeMemWr
-- Engineer: Fearghal Morgan, National University of Ireland, Galway
-- Date: 9/1/2021
-- Description

-- generate memory component write signal from input signal memWr and memAdd(2:0) (= hostMemAdd(7:5))  
-- Signal data dictionary
--  Active host or DSP_top write access to memory
--  memWr        write signal selected from host or DSP_top   
--  memAdd       memory bank address, selecting memory component  
--  Output signals
--     BRAM_we            assertion (h) synchronously performs write to addressed 32 x 32-byte BRAM  
--     reg4x32_CSRA_we    assertion (h) synchronously performs write to addressed 4 x 32-bit register array
--     reg32x32_we        assertion (h) synchronously performs write to addressed 32 x 32-byte register array 
--  host  write access to memory
--  host_memWr            write signal selected from host or DSP_top   
--  host_memAdd           host memory address  
--  Output signal
--     reg4x32_CSRB_we    assertion (h) synchronously performs write to addressed 4 x 32-byte register array 
    
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use work.arrayPackage.all;

entity decodeMemWr is
    Port ( memWr            : in  std_logic;
	       memAdd		    : in  std_logic_vector(10 downto 0);
           BRAM_we          : out std_logic;
		   reg32x32_we      : out std_logic;
           reg4x32_CSRA_we  : out std_logic;

           host_memWr       : in  std_logic;
           host_memAdd      : in  std_logic_vector(10 downto 0);
           reg4x32_CSRB_we  : out std_logic
    	  );
end decodeMemWr;

architecture comb of decodeMemWr is
-- signals used in vicilogic -- could be omitted from model
constant BRAM_add_7DT5          : std_logic_vector(2 downto 0) := "001";
constant reg32x32_add_7DT5      : std_logic_vector(2 downto 0) := "010";
constant reg4x32_CSRA_add_7DT5  : std_logic_vector(2 downto 0) := "000";
constant reg4x32_CSRB_add_7DT5  : std_logic_vector(2 downto 0) := "011";

begin

decodeMemoryWr_i: process (memWr, memAdd, host_memWr, host_memAdd)
begin 
  BRAM_we          <= '0'; -- defaults
  reg32x32_we      <= '0'; 
  reg4x32_CSRA_we  <= '0'; 

  reg4x32_CSRB_we  <= '0'; 

  if memWr = '1' then -- these memory components are write accessible by active host or DSP_top
    if    memAdd(7 downto 5) = reg4x32_CSRA_add_7DT5 then        
		reg4x32_CSRA_we <= '1';
    elsif memAdd(7 downto 5) = BRAM_add_7DT5 then  
	    BRAM_we          <= '1'; 
    elsif memAdd(7 downto 5) = reg32x32_add_7DT5 then  
    	reg32x32_we      <= '1'; 
	end if;
  end if;
  
  if host_memWr = '1' then -- this memory component is always write accessible by host 
	if host_memAdd(7 downto 5) = reg4x32_CSRB_add_7DT5 then 
    	reg4x32_CSRB_we <= '1'; 
	end if;
  end if;
end process;

end comb;