import sys
import pymysql

# Inject PyMySQL as a drop-in replacement for mysqlclient
pymysql.install_as_MySQLdb()

# Spoof mysqlclient version checks to satisfy modern Django versions
sys.modules['MySQLdb'].__version__ = '2.2.1'
sys.modules['MySQLdb'].version_info = (2, 2, 1, 'final', 0)
