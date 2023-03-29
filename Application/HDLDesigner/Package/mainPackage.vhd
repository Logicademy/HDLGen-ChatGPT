-- Package
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package arrayPackage is
type array3x32 is array(3 downto 0) of std_logic_vector(32 downto 0);
type array4x32 is array(4 downto 0) of std_logic_vector(32 downto 0);
type reg4x4_Array is array(4 downto 0) of std_logic_vector(4 downto 0);


end arrayPackage;
package body arrayPackage is
end arrayPackage;

