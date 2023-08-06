# encoding: utf-8
'''
@project: djangoModel->StandingBookServices
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 台账服务
@created_time: 2023/3/24 10:07
'''
from xj_enroll.api.enroll_apis import EnrollAPI
from xj_enroll.service.enroll_record_serivce import EnrollRecordServices
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from xj_role.services.user_group_service import UserGroupService
from xj_user.services.user_relate_service import UserRelateToUserService
from ..utils.join_list import JoinList


class StandingBookServices():
    @staticmethod
    def standing_book(params: dict = None):
        """
        请求参数：params
        :param params: 筛选参数
        :return: list,err
        """
        page = int(params.get("page", 1))
        size = int(params.get("size", 10))

        enroll_result, err = EnrollAPI.list_handle(request_params=params)
        enroll_list = enroll_result['list']
        user_id_list = list(set([i['user_id'] for i in enroll_list]))
        enroll_id_list = list(set([i['id'] for i in enroll_list]))
        # 权限模块获取部门
        group_names, err = UserGroupService.get_user_group_info(user_id_list=user_id_list, field_list=['group_name', 'user_id'])
        # 获取业务人员
        beneficiary_users, err = UserRelateToUserService.list(params={'relate_key': 'beneficiary', "user_id_list": user_id_list, 'need_pagination': 0})
        beneficiary_user_map = {i["user_id"]: i["with_user_name"] for i in beneficiary_users or []}
        # 获取接单人员
        enroll_record_list, err = EnrollRecordServices.record_list(params={"enroll_id_list": enroll_id_list}, need_pagination=False)
        enroll_record_map = {}
        for i in enroll_record_list:
            if enroll_record_map.get(i["enroll"]):
                enroll_record_map[i["enroll"]].append(i["user_info"]["full_name"])
            else:
                enroll_record_map[i["enroll"]] = [i["user_info"]["full_name"]]
        current_index = (page - 1) * size
        # 获取发票相关的信息
        for item in enroll_list:
            # 添加
            group_names_str = ""
            for i in group_names.get(item["user_id"], []):
                group_names_str = group_names_str + ("," if len(group_names_str) > 0 else "") + i["group_name"]
            item["group_name"] = "游客" if not group_names_str else group_names_str  # 分组字符串

            current_index += 1
            item["index"] = current_index  # 序号
            item["beneficiary"] = beneficiary_user_map.get(item["user_id"], "非业务人员邀请用户")  # 邀请用户
            item["total"] = item["count"] * item["price"]  # 小计
            item["beneficiary_amount"] = float(item["amount"]) * 0.6  # 业务员提成
            item["urge_free"] = 50 if isinstance(item["is_urgent"], str) and int(item["is_urgent"]) else 0  # 加急费用
            item["other_money"] = '-'  # 其他款项

            enroll_user_name_str = ""
            for i in enroll_record_map.get(item["id"], []):
                enroll_user_name_str = enroll_user_name_str + ("," if len(enroll_user_name_str) > 0 else "") + i
            item["enroll_user_names"] = enroll_user_name_str  # 报名名称

        enroll_result['list'] = enroll_list
        # 资金相关的数据
        finance_list, err = FinanceTransactsService.finance_standing_book(params={"enroll_id_list": enroll_id_list})
        JoinList.left_join(l_list=enroll_result['list'], r_list=finance_list, l_key="id", r_key="enroll_id")
        return enroll_result, None
