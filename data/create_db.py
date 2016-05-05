import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
sql = """create table `member` (
`id` integer primary key AUTOINCREMENT,
`member_id` varchar(40) NOT NULL,
`fullname` varchar(40) NOT NULL,
`email` varchar(200) NOT NULL, 
`url_token` varchar(200) NOT NULL,
`password` char(40) NOT NULL,
`headline` varchar(140) DEFAULT NULL,
`confirm_key` varchar(20) NOT NULL,
`active` int(2) NOT NULL DEFAULT '0',
`banned` tinyint(2) NOT NULL DEFAULT '0',
`sina_info_id` int(11) DEFAULT NULL,
`douban_info_id` int(11) DEFAULT NULL,
`is_admin` int(2) NOT NULL DEFAULT '0',
`custom_url_updated` int(10) NOT NULL DEFAULT '0',
`created` int(10) NOT NULL DEFAULT '0',
`last_updated` int(10) NOT NULL DEFAULT '0',
`invitation_key_num` int(10) NOT NULL DEFAULT '0',
`avatar_path` varchar(30) DEFAULT NULL,
`reset_key` varchar(20) DEFAULT NULL,
`reset_expires` int(11) DEFAULT NULL,
`can_invite` tinyint(2) NOT NULL DEFAULT '1',
`muted` int(2) NOT NULL DEFAULT '0',
`status` int(2) NOT NULL DEFAULT '0',
`name_updated` int(10) NOT NULL DEFAULT '0'
)"""
cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()

