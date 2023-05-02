-- Model name: datapathGenerator  
-- Description: Data generation component

-- Complete all sections marked >>
-- >> Authors: 
-- >> Date: 

-- Signal dictionary 
-- Inputs
--   selCtrl      deassert (l) to select ctrlA as DPMux select signal 
--                assert   (h) to select ctrlB as DPMux select signal 
--   ctrlA        2-bit control bus
--   ctrlB        2-bit control bus
--   sig0Dat      1-bit data  
--   sig1Dat      3-bit bus data
--   sig2Dat      8-bit bus data
--   sig3Dat      4-bit bus data
-- Outputs         
--   datA         8-bit data 
--   datB         8-bit data. 2s complement of datA 
--   datC         8-bit data. datA + datB

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.all;
 
entity datapathGenerator is
    Port ( selCtrl     : in  std_logic;
           ctrlA       : in  STD_LOGIC_VECTOR(1 downto 0);
           ctrlB       : in  STD_LOGIC_VECTOR(1 downto 0);  
           sys0Dat     : in  STD_LOGIC;   
           sys1Dat     : in  STD_LOGIC_VECTOR(2 downto 0);   
           sys2Dat     : in  STD_LOGIC_VECTOR(7 downto 0);
           sys3Dat     : in  STD_LOGIC_VECTOR(3 downto 0);
           datA        : out STD_LOGIC_VECTOR(7 downto 0);
           datB        : out STD_LOGIC_VECTOR(7 downto 0);
           datC        : out STD_LOGIC_VECTOR(7 downto 0)
          );
end datapathGenerator;

architecture combinational of datapathGenerator is
-- >> declare internal signals  

begin

-- >> complete VHDL model, using signals exactly as defined in the datapathGenerator specification

end combinational;