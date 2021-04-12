from database import CursorFromConnectionFromPool

class QueryNu:
    def __init__(self, IPRange, ConvertID, id):
        self.id = id
        self.IPRange = IPRange
        self.ConvertID = ConvertID

    def __repr__(self):
        return "<Conversion ID: {} | IP Range: {} | id: {} >".format(self.ConvertID, self.IPRange, self.id)

    def save_to_db(self):
        with CursorFromConnectionFromPool as cursor:
            cursor.execute('INSERT INTO input_table (IPRange, ConvertID) VALUES (%s, %s)',
                           (self.IPRange, self.ConvertID))


    @classmethod
    def converter_addrip(cls,IPRange,ConvertID):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT DISTINCT ON '
                '(conversion_id,ip, netmask,comment, orig_name, orig_if, mapped_if, self_gen, display_cli, convert_status, orig_config, is_wildcard, global_level, allow_routing, color) '
                'ip,netmask,name from converter_addrip '
                'WHERE conversion_id = %s AND %s::inet >> ip::inet',
                (ConvertID, IPRange,)
            )
            converter_addrip_output = cursor.fetchall()
            return converter_addrip_output

    @staticmethod
    def converter_addrip_name(addrip_name,ConvertID):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT DISTINCT ON '
                '(conversion_id,ip, netmask,comment, orig_name, orig_if, mapped_if, self_gen, display_cli, convert_status, orig_config, is_wildcard, global_level, allow_routing, color) '
                '* from converter_addrip '
                'WHERE conversion_id = %s AND name = %s',
                (ConvertID, addrip_name,)
            )
            converter_addrip_name = cursor.fetchall()
            return converter_addrip_name

    @staticmethod
    def converter_addrgrp(addrip,ConvertID):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT DISTINCT ON '
                '(conversion_id,name,comment,orig_name,member,orig_if,mapped_if,display_cli,mixedipv4andipv6,convert_status,orig_config,global_level,src_or_dst,allow_routing,color,exclude,exclude_member) '
                '* FROM converter_addrgrp WHERE conversion_id = %s AND POSITION( %s IN member) != 0',
                (ConvertID, addrip,))
            converter_addrgrp_output = cursor.fetchall()
            return converter_addrgrp_output

    @staticmethod
    def converter_policy(addripgrp,ConvertID):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT DISTINCT ON '
                '(conversion_id,name,package,orig_name,status,action,schedule,log_traffic,log_traffic_start,comment,vpn_group,label,auto_gen_comment,nat_ip,nat_ip_mask,global_location,dscp,original,nat_type,src_intf,dst_intf,vpn_tunnel,src_addr,dst_addr,service,pool_name,user,install,implied_object,gen_comment,self_traffic_addr,vpn_enable,nat_outbound,nat_inbound,pair_policy,src_negate,dst_negate,fixed_port,dst_all_static,self_traffic_policy,comment_out,display_cli,nat_correlation,display_order,orig_config,vpn_name,prev_name,devices,mainpolicyid,subpolicyid,dst_addr6,src_addr6,send_deny_packet,pan_warning,application,undefined_obj) '
                '* FROM converter_policy WHERE conversion_id = %s AND (POSITION ( %s IN src_addr) != 0 OR POSITION ( %s IN dst_addr) != 0)',
                (ConvertID, addripgrp, addripgrp,))
            converter_policy_output = cursor.fetchall()
            return converter_policy_output

    @staticmethod
    def converter_origpolicycombination(addripgrp,ConvertID):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute(
                'SELECT DISTINCT ON '
                '(conversion_id,orig_config,convert_status,name,src_addr,dst_addr,service,orig_dst_addr,orig_service,orig_src_addr) '
                '* FROM converter_origpolicycombination WHERE conversion_id = %s AND (POSITION ( %s IN src_addr) != 0 OR POSITION ( %s IN dst_addr) != 0 OR POSITION ( %s IN orig_src_addr) != 0 OR POSITION ( %s IN orig_dst_addr) != 0)',
                (ConvertID, addripgrp, addripgrp, addripgrp, addripgrp,))
            converter_origpolicycombination_output = cursor.fetchall()
            return converter_origpolicycombination_output
