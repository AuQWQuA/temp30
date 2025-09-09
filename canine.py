"""
犬科动物类模块
继承自Mammal哺乳动物类，添加犬科动物特有的属性和行为
包括狗、狼、狐狸等犬科动物的共同特征
"""

import datetime
import random
import math
from typing import Optional, List, Dict, Any, Tuple
from mammal import Mammal, AnimalRecord


class PackBehavior:
    """群体行为管理类"""
    
    def __init__(self):
        self.pack_members: List[str] = []  # 存储群体成员ID
        self.pack_role = "成员"  # 首领, 副首领, 成员, 幼崽
        self.dominance_level = 50  # 支配等级 0-100
        self.loyalty_bonds: Dict[str, int] = {}  # 与其他成员的忠诚度
        self.territorial_markings: List[Dict[str, Any]] = []
        self.hunting_contributions = 0
        self.pack_hierarchy_changes: List[AnimalRecord] = []
    
    def join_pack(self, pack_member_ids: List[str], initial_role: str = "成员"):
        """加入群体"""
        self.pack_members = pack_member_ids.copy()
        self.pack_role = initial_role
        
        # 为每个成员建立初始忠诚度
        for member_id in pack_member_ids:
            self.loyalty_bonds[member_id] = random.randint(30, 70)
        
        record = AnimalRecord('pack_join', f"加入群体，角色: {initial_role}")
        self.pack_hierarchy_changes.append(record)
    
    def leave_pack(self, reason: str = "自然离开"):
        """离开群体"""
        former_members = self.pack_members.copy()
        self.pack_members.clear()
        self.pack_role = "独行者"
        self.loyalty_bonds.clear()
        
        record = AnimalRecord('pack_leave', f"离开群体，原因: {reason}")
        self.pack_hierarchy_changes.append(record)
        
        return {'former_pack_size': len(former_members), 'reason': reason}
    
    def challenge_hierarchy(self, target_member_id: str) -> Dict[str, Any]:
        """挑战群体等级"""
        if target_member_id not in self.pack_members:
            return {'status': 'error', 'message': '目标不在群体中'}
        
        if self.pack_role == "幼崽":
            return {'status': 'error', 'message': '幼崽不能挑战等级'}
        
        # 计算挑战成功率
        base_success_rate = 0.3
        dominance_factor = self.dominance_level / 100
        success_rate = base_success_rate + dominance_factor * 0.4
        
        if random.random() <= success_rate:
            # 挑战成功
            old_role = self.pack_role
            if self.pack_role == "成员":
                self.pack_role = "副首领"
            elif self.pack_role == "副首领":
                self.pack_role = "首领"
            
            self.dominance_level = min(100, self.dominance_level + 15)
            
            record = AnimalRecord('hierarchy_challenge', f"成功挑战，从{old_role}晋升为{self.pack_role}")
            self.pack_hierarchy_changes.append(record)
            
            return {
                'status': 'success',
                'old_role': old_role,
                'new_role': self.pack_role,
                'dominance_change': 15
            }
        else:
            # 挑战失败
            self.dominance_level = max(0, self.dominance_level - 10)
            
            record = AnimalRecord('hierarchy_challenge', f"挑战{target_member_id}失败")
            self.pack_hierarchy_changes.append(record)
            
            return {
                'status': 'failed',
                'dominance_change': -10,
                'consequences': '地位下降'
            }
    
    def mark_territory(self, location: str, marking_type: str = "尿液标记"):
        """标记领地"""
        marking = {
            'location': location,
            'type': marking_type,
            'timestamp': datetime.datetime.now(),
            'strength': random.uniform(0.7, 1.0)  # 标记强度
        }
        
        self.territorial_markings.append(marking)
        
        # 增加支配等级
        self.dominance_level = min(100, self.dominance_level + 2)
    
    def coordinate_hunt(self, prey_size: str, pack_size: int) -> Dict[str, Any]:
        """协调群体狩猎"""
        if not self.pack_members:
            return {'status': 'error', 'message': '没有群体成员'}
        
        # 根据猎物大小和群体规模计算成功率
        base_success_rates = {
            '小型': 0.8,
            '中型': 0.6,
            '大型': 0.4
        }
        
        base_rate = base_success_rates.get(prey_size, 0.6)
        pack_bonus = min(0.3, pack_size * 0.05)  # 群体协作加成
        role_bonus = {'首领': 0.1, '副首领': 0.05, '成员': 0, '幼崽': -0.1}.get(self.pack_role, 0)
        
        success_rate = base_rate + pack_bonus + role_bonus
        
        if random.random() <= success_rate:
            self.hunting_contributions += 1
            return {
                'status': 'success',
                'prey_size': prey_size,
                'pack_coordination': 'excellent',
                'individual_contribution': 'significant'
            }
        else:
            return {
                'status': 'failed',
                'prey_size': prey_size,
                'pack_coordination': 'poor',
                'learning_opportunity': True
            }


class CommunicationSystem:
    """犬科动物交流系统"""
    
    def __init__(self):
        self.vocal_repertoire: List[str] = []
        self.body_language_signals: Dict[str, str] = {}
        self.scent_communications: List[Dict[str, Any]] = []
        self.communication_records: List[AnimalRecord] = []
        self.hearing_acuity = 85  # 听觉敏锐度 0-100
        self.vocal_volume = 70   # 发声音量 0-100
    
    def learn_vocalization(self, sound_type: str, meaning: str):
        """学习新的发声"""
        if sound_type not in self.vocal_repertoire:
            self.vocal_repertoire.append(sound_type)
            self.body_language_signals[sound_type] = meaning
            
            record = AnimalRecord('vocal_learning', f"学会新发声: {sound_type} - {meaning}")
            self.communication_records.append(record)
    
    def howl(self, purpose: str = "群体召集", duration_seconds: int = 30) -> Dict[str, Any]:
        """嚎叫"""
        if "嚎叫" not in self.vocal_repertoire:
            self.learn_vocalization("嚎叫", "远距离交流")
        
        # 嚎叫的传播距离
        transmission_distance_km = (self.vocal_volume / 100) * 10
        
        # 根据目的调整效果
        effects = {
            '群体召集': {'loyalty_boost': 10, 'pack_coordination': 15},
            '警告': {'territorial_strength': 20, 'intimidation': 25},
            '寻找伴侣': {'attraction_range_km': transmission_distance_km * 1.5},
            '表达情感': {'happiness_change': 5, 'stress_relief': 10}
        }
        
        effect = effects.get(purpose, effects['群体召集'])
        
        record = AnimalRecord('howl', f"嚎叫{duration_seconds}秒，目的: {purpose}")
        self.communication_records.append(record)
        
        return {
            'sound_type': '嚎叫',
            'purpose': purpose,
            'duration_seconds': duration_seconds,
            'transmission_distance_km': round(transmission_distance_km, 1),
            'effects': effect
        }
    
    def bark(self, intensity: str = "中等", message_type: str = "警戒") -> Dict[str, Any]:
        """吠叫"""
        if "吠叫" not in self.vocal_repertoire:
            self.learn_vocalization("吠叫", "警报和交流")
        
        intensity_levels = {
            '轻微': {'volume_modifier': 0.5, 'energy_cost': 2},
            '中等': {'volume_modifier': 1.0, 'energy_cost': 5},
            '强烈': {'volume_modifier': 1.5, 'energy_cost': 8}
        }
        
        level = intensity_levels.get(intensity, intensity_levels['中等'])
        actual_volume = self.vocal_volume * level['volume_modifier']
        
        record = AnimalRecord('bark', f"{intensity}吠叫，传达: {message_type}")
        self.communication_records.append(record)
        
        return {
            'sound_type': '吠叫',
            'intensity': intensity,
            'message': message_type,
            'effective_volume': round(actual_volume, 1),
            'energy_cost': level['energy_cost']
        }
    
    def use_body_language(self, signal_type: str, target: str = "群体") -> Dict[str, Any]:
        """使用肢体语言"""
        body_signals = {
            '尾巴摆动': {'meaning': '友好/兴奋', 'intensity': 'positive'},
            '耳朵竖立': {'meaning': '警觉/注意', 'intensity': 'alert'},
            '露出牙齿': {'meaning': '威胁/警告', 'intensity': 'aggressive'},
            '低头服从': {'meaning': '服从/顺从', 'intensity': 'submissive'},
            '背毛竖立': {'meaning': '恐惧/威胁', 'intensity': 'defensive'},
            '趴伏邀请': {'meaning': '游戏邀请', 'intensity': 'playful'}
        }
        
        signal_info = body_signals.get(signal_type, {'meaning': '未知信号', 'intensity': 'neutral'})
        
        record = AnimalRecord('body_language', f"向{target}展示{signal_type}")
        self.communication_records.append(record)
        
        return {
            'signal': signal_type,
            'meaning': signal_info['meaning'],
            'intensity': signal_info['intensity'],
            'target': target,
            'effectiveness': random.uniform(0.7, 1.0)
        }
    
    def leave_scent_message(self, location: str, message_type: str = "身份标识"):
        """留下气味信息"""
        scent_message = {
            'location': location,
            'message_type': message_type,
            'timestamp': datetime.datetime.now(),
            'persistence_hours': random.randint(12, 72),  # 气味持续时间
            'information_content': self._generate_scent_content()
        }
        
        self.scent_communications.append(scent_message)
        
        record = AnimalRecord('scent_marking', f"在{location}留下{message_type}气味信息")
        self.communication_records.append(record)
    
    def _generate_scent_content(self) -> Dict[str, Any]:
        """生成气味信息内容"""
        return {
            'identity': '个体标识',
            'health_status': random.choice(['健康', '一般', '虚弱']),
            'emotional_state': random.choice(['平静', '兴奋', '紧张']),
            'recent_activities': random.choice(['狩猎', '休息', '游戏']),
            'territorial_claim': random.choice(['强', '中', '弱'])
        }


class Canine(Mammal):
    """
    犬科动物类
    继承自Mammal哺乳动物类，包含犬科动物特有的特征和行为
    """
    
    # 类变量
    canine_count = 0
    pack_formation_threshold = 3  # 形成群体的最小数量
    
    def __init__(self, name: str, species: str, age: int, weight: float,
                 owner: str = "未知", gender: str = "未知", 
                 fur_color: str = "棕色", fur_type: str = "双层毛",
                 bite_force_psi: float = 200.0, pack_instinct: bool = True):
        
        # 调用父类构造函数
        super().__init__(name, species, age, weight, owner, gender, fur_color, fur_type)
        
        # 犬科动物特有属性
        self.bite_force_psi = bite_force_psi
        self.pack_instinct = pack_instinct
        self.tail_length_cm = self._calculate_tail_length()
        self.ear_type = random.choice(["竖立", "下垂", "半竖"])
        self.snout_length_cm = self._calculate_snout_length()
        
        # 感官能力（增强版）
        self.smell_sensitivity = "极高"
        self.hearing_range_hz = (40, 60000)  # 犬科动物听觉范围更广
        self.night_vision_quality = "优秀"
        
        # 行为特征
        self.loyalty_level = random.randint(70, 95)
        self.territorial_instinct = random.randint(60, 90)
        self.hunting_drive = random.randint(50, 95)
        self.playfulness = random.randint(40, 85)
        
        # 专门的管理系统
        self.pack_behavior = PackBehavior()
        self.communication = CommunicationSystem()
        
        # 犬科特有行为数据
        self.digging_spots: List[Dict[str, Any]] = []
        self.buried_items: List[Dict[str, Any]] = []
        self.tracking_records: List[AnimalRecord] = []
        self.play_sessions: List[Dict[str, Any]] = []
        
        # 训练和学习能力
        self.trainability_score = random.randint(60, 95)
        self.learned_commands: List[str] = []
        self.training_sessions: List[AnimalRecord] = []
        
        # 狩猎和追踪技能
        self.scent_tracking_ability = random.randint(80, 98)
        self.pursuit_endurance_km = random.uniform(5, 25)
        self.cooperative_hunting_skill = random.randint(70, 95) if pack_instinct else random.randint(30, 60)
        
        # 初始化基本发声能力
        self.communication.learn_vocalization("吠叫", "基本交流")
        self.communication.learn_vocalization("呜咽", "请求或痛苦")
        if pack_instinct:
            self.communication.learn_vocalization("嚎叫", "群体交流")
        
        # 更新计数
        Canine.canine_count += 1
        
        # 记录犬科动物特有信息
        self._log_activity("犬科动物创建", f"犬科动物{self.name}已注册，咬合力: {self.bite_force_psi} PSI")
    
    def _calculate_tail_length(self) -> float:
        """计算尾巴长度"""
        # 基于体重估算尾巴长度
        base_length = math.sqrt(self.weight) * 8
        variation = random.uniform(0.8, 1.2)
        return round(base_length * variation, 1)
    
    def _calculate_snout_length(self) -> float:
        """计算口吻长度"""
        # 基于头部大小估算
        head_size_factor = math.log(self.weight + 1) * 3
        variation = random.uniform(0.9, 1.1)
        return round(head_size_factor * variation, 1)
    
    def track_scent(self, scent_type: str, age_hours: int, difficulty: str = "中等") -> Dict[str, Any]:
        """追踪气味"""
        if not self.is_alive:
            return {'status': 'error', 'message': '动物已死亡'}
        
        if self.energy_level < 20:
            return {'status': 'insufficient_energy', 'message': '能量不足，无法追踪'}
        
        # 计算追踪成功率
        base_success_rate = self.scent_tracking_ability / 100
        age_penalty = min(0.5, age_hours * 0.02)  # 气味越老越难追踪
        difficulty_penalties = {'简单': 0, '中等': 0.1, '困难': 0.2, '极难': 0.3}
        difficulty_penalty = difficulty_penalties.get(difficulty, 0.1)
        
        success_rate = base_success_rate - age_penalty - difficulty_penalty
        success_rate = max(0.1, success_rate)  # 最低10%成功率
        
        # 消耗能量
        energy_cost = 15 + (age_hours * 0.5) + (difficulty_penalties.get(difficulty, 0.1) * 50)
        self.energy_level = max(0, self.energy_level - energy_cost)
        
        if random.random() <= success_rate:
            # 追踪成功
            distance_tracked = random.uniform(0.5, self.pursuit_endurance_km * 0.3)
            tracking_time = distance_tracked / 3  # 假设3公里/小时的追踪速度
            
            self.happiness_level = min(100, self.happiness_level + 15)
            
            record = AnimalRecord('tracking_success', f"成功追踪{scent_type}，距离{distance_tracked:.1f}公里")
            self.tracking_records.append(record)
            
            return {
                'status': 'success',
                'scent_type': scent_type,
                'distance_tracked_km': round(distance_tracked, 1),
                'tracking_time_hours': round(tracking_time, 1),
                'trail_quality': 'clear' if success_rate > 0.7 else 'faint'
            }
        else:
            # 追踪失败
            self.happiness_level = max(0, self.happiness_level - 8)
            
            record = AnimalRecord('tracking_failed', f"追踪{scent_type}失败")
            self.tracking_records.append(record)
            
            return {
                'status': 'failed',
                'scent_type': scent_type,
                'reason': 'trail_lost',
                'energy_wasted': energy_cost
            }
    
    def dig_hole(self, purpose: str = "藏食物", depth_cm: int = 30) -> Dict[str, Any]:
        """挖洞"""
        if not self.is_alive:
            return {'status': 'error', 'message': '动物已死亡'}
        
        if self.energy_level < 25:
            return {'status': 'insufficient_energy', 'message': '能量不足，无法挖洞'}
        
        # 挖洞消耗能量
        energy_cost = depth_cm * 0.5
        self.energy_level = max(0, self.energy_level - energy_cost)
        
        # 创建挖洞记录
        dig_spot = {
            'location': f"位置_{len(self.digging_spots) + 1}",
            'purpose': purpose,
            'depth_cm': depth_cm,
            'timestamp': datetime.datetime.now(),
            'success': True
        }
        
        self.digging_spots.append(dig_spot)
        
        # 挖洞带来的满足感
        self.happiness_level = min(100, self.happiness_level + 10)
        
        self._log_activity("挖洞", f"挖了一个{depth_cm}厘米深的洞，用途: {purpose}")
        
        return {
            'status': 'success',
            'location': dig_spot['location'],
            'depth_cm': depth_cm,
            'purpose': purpose,
            'energy_consumed': energy_cost
        }
    
    def bury_item(self, item: str, location: str = None) -> Dict[str, Any]:
        """埋藏物品"""
        if not location:
            # 寻找现有的洞或挖新洞
            if self.digging_spots:
                available_spots = [spot for spot in self.digging_spots if spot['purpose'] in ['藏食物', '储存']]
                if available_spots:
                    location = available_spots[-1]['location']
                else:
                    dig_result = self.dig_hole("储存", 25)
                    if dig_result['status'] == 'success':
                        location = dig_result['location']
                    else:
                        return dig_result
            else:
                dig_result = self.dig_hole("储存", 25)
                if dig_result['status'] == 'success':
                    location = dig_result['location']
                else:
                    return dig_result
        
        buried_item = {
            'item': item,
            'location': location,
            'burial_date': datetime.datetime.now(),
            'retrieval_date': None,
            'condition': '新鲜'
        }
        
        self.buried_items.append(buried_item)
        
        self._log_activity("埋藏", f"在{location}埋藏了{item}")
        
        return {
            'status': 'success',
            'item': item,
            'location': location,
            'burial_time': buried_item['burial_date'].strftime('%Y-%m-%d %H:%M')
        }
    
    def retrieve_buried_item(self, item: str = None, location: str = None) -> Dict[str, Any]:
        """挖取埋藏的物品"""
        if not self.buried_items:
            return {'status': 'not_found', 'message': '没有埋藏的物品'}
        
        # 查找要挖取的物品
        target_items = []
        for buried_item in self.buried_items:
            if buried_item['retrieval_date'] is None:  # 还没有被挖取
                if item and buried_item['item'] == item:
                    target_items.append(buried_item)
                elif location and buried_item['location'] == location:
                    target_items.append(buried_item)
                elif not item and not location:
                    target_items.append(buried_item)
        
        if not target_items:
            return {'status': 'not_found', 'message': '找不到指定的埋藏物品'}
        
        # 选择一个物品挖取
        retrieved_item = random.choice(target_items)
        retrieved_item['retrieval_date'] = datetime.datetime.now()
        
        # 计算物品状态
        burial_duration_days = (retrieved_item['retrieval_date'] - retrieved_item['burial_date']).days
        if burial_duration_days > 7:
            retrieved_item['condition'] = '变质'
        elif burial_duration_days > 3:
            retrieved_item['condition'] = '一般'
        else:
            retrieved_item['condition'] = '良好'
        
        self.happiness_level = min(100, self.happiness_level + 12)
        
        self._log_activity("挖取", f"从{retrieved_item['location']}挖取了{retrieved_item['item']}")
        
        return {
            'status': 'success',
            'item': retrieved_item['item'],
            'location': retrieved_item['location'],
            'condition': retrieved_item['condition'],
            'burial_duration_days': burial_duration_days
        }
    
    def play_with_object(self, object_type: str = "球", duration_minutes: int = 15) -> Dict[str, Any]:
        """与物品玩耍"""
        if not self.is_alive:
            return {'status': 'error', 'message': '动物已死亡'}
        
        if self.energy_level < 15:
            return {'status': 'insufficient_energy', 'message': '太累了，无法玩耍'}
        
        # 消耗能量，但增加快乐度
        energy_cost = duration_minutes * 0.8
        happiness_gain = duration_minutes * 1.2 + (self.playfulness / 10)
        
        self.energy_level = max(0, self.energy_level - energy_cost)
        self.happiness_level = min(100, self.happiness_level + happiness_gain)
        
        # 记录游戏会话
        play_session = {
            'object': object_type,
            'duration_minutes': duration_minutes,
            'timestamp': datetime.datetime.now(),
            'enjoyment_level': random.uniform(0.7, 1.0),
            'energy_spent': energy_cost
        }
        
        self.play_sessions.append(play_session)
        
        self._log_activity("游戏", f"与{object_type}玩耍{duration_minutes}分钟")
        
        return {
            'status': 'success',
            'object': object_type,
            'duration_minutes': duration_minutes,
            'happiness_gained': round(happiness_gain, 1),
            'energy_consumed': round(energy_cost, 1),
            'fun_level': 'high' if play_session['enjoyment_level'] > 0.8 else 'moderate'
        }
    
    def learn_command(self, command: str, trainer: str = "主人", repetitions: int = 10) -> Dict[str, Any]:
        """学习新命令"""
        if command in self.learned_commands:
            return {'status': 'already_known', 'message': f'已经学会了{command}命令'}
        
        # 学习成功率基于训练能力和重复次数
        base_success_rate = self.trainability_score / 100
        repetition_bonus = min(0.3, repetitions * 0.02)
        success_rate = base_success_rate + repetition_bonus
        
        # 年龄影响学习能力
        if self.age > 8:
            success_rate *= 0.8  # 老年犬学习较慢
        elif self.age < 2:
            success_rate *= 1.2  # 幼犬学习较快
        
        success_rate = min(0.95, success_rate)  # 最高95%成功率
        
        if random.random() <= success_rate:
            # 学会了命令
            self.learned_commands.append(command)
            self.happiness_level = min(100, self.happiness_level + 8)
            
            record = AnimalRecord('command_learned', f"学会了'{command}'命令，经过{repetitions}次重复")
            self.training_sessions.append(record)
            
            return {
                'status': 'success',
                'command': command,
                'repetitions_needed': repetitions,
                'trainer': trainer,
                'mastery_level': 'basic'
            }
        else:
            # 没有学会，但有进步
            record = AnimalRecord('training_attempt', f"尝试学习'{command}'命令，需要更多练习")
            self.training_sessions.append(record)
            
            return {
                'status': 'progress',
                'command': command,
                'repetitions_completed': repetitions,
                'suggestion': '需要更多重复练习'
            }
    
    def obey_command(self, command: str) -> Dict[str, Any]:
        """执行命令"""
        if command not in self.learned_commands:
            return {'status': 'unknown_command', 'message': f'不认识{command}命令'}
        
        # 执行成功率基于忠诚度和能量水平
        base_obedience_rate = self.loyalty_level / 100
        energy_factor = self.energy_level / 100
        success_rate = base_obedience_rate * 0.7 + energy_factor * 0.3
        
        if random.random() <= success_rate:
            # 成功执行命令
            self.happiness_level = min(100, self.happiness_level + 5)
            
            # 某些命令有特殊效果
            command_effects = {
                '坐下': {'energy_change': 2, 'discipline': 1},
                '握手': {'happiness_change': 3, 'social_bond': 2},
                '趴下': {'energy_change': 3, 'calm': 1},
                '来': {'exercise': 5, 'loyalty_boost': 1},
                '停': {'discipline': 2, 'self_control': 1}
            }
            
            effects = command_effects.get(command, {})
            
            self._log_activity("命令执行", f"成功执行'{command}'命令")
            
            return {
                'status': 'success',
                'command': command,
                'execution_quality': 'excellent' if success_rate > 0.8 else 'good',
                'effects': effects
            }
        else:
            # 没有执行或执行不当
            self._log_activity("命令执行", f"尝试执行'{command}'命令但失败")
            
            return {
                'status': 'failed',
                'command': command,
                'reason': 'distracted' if self.energy_level > 50 else 'too_tired'
            }
    
    def form_pack_with(self, other_canines: List['Canine']) -> Dict[str, Any]:
        """与其他犬科动物组成群体"""
        if not self.pack_instinct:
            return {'status': 'error', 'message': '缺乏群体本能'}
        
        if len(other_canines) < 1:
            return {'status': 'insufficient_members', 'message': '需要至少1个其他成员'}
        
        # 检查其他成员是否也有群体本能
        eligible_members = [canine for canine in other_canines if canine.pack_instinct and canine.is_alive]
        
        if len(eligible_members) < 1:
            return {'status': 'no_eligible_members', 'message': '没有合适的群体成员'}
        
        # 组建群体
        pack_member_ids = [canine.animal_id for canine in eligible_members] + [self.animal_id]
        
        # 确定群体角色
        all_canines = eligible_members + [self]
        all_canines.sort(key=lambda x: (x.age, x.weight, x.dominance_level), reverse=True)
        
        for i, canine in enumerate(all_canines):
            if i == 0:
                role = "首领"
            elif i == 1 and len(all_canines) > 2:
                role = "副首领"
            else:
                role = "成员"
            
            canine.pack_behavior.join_pack(pack_member_ids, role)
        
        self._log_activity("群体形成", f"与{len(eligible_members)}只犬科动物组成群体")
        
        return {
            'status': 'success',
            'pack_size': len(pack_member_ids),
            'pack_members': [{'id': canine.animal_id, 'name': canine.name, 'role': canine.pack_behavior.pack_role} 
                           for canine in all_canines],
            'alpha': all_canines[0].get_basic_info()
        }
    
    def hunt_as_pack(self, prey_type: str, prey_size: str = "中型") -> Dict[str, Any]:
        """群体狩猎"""
        if not self.pack_behavior.pack_members:
            return self.hunt_prey(prey_type, 0.4)  # 单独狩猎成功率较低
        
        pack_size = len(self.pack_behavior.pack_members)
        hunt_result = self.pack_behavior.coordinate_hunt(prey_size, pack_size)
        
        if hunt_result['status'] == 'success':
            # 群体狩猎成功，分配收益
            base_energy_gain = {'小型': 30, '中型': 50, '大型': 80}.get(prey_size, 50)
            individual_share = base_energy_gain / pack_size
            
            # 根据角色调整分配
            role_multipliers = {'首领': 1.3, '副首领': 1.1, '成员': 1.0, '幼崽': 0.8}
            role_multiplier = role_multipliers.get(self.pack_behavior.pack_role, 1.0)
            
            energy_gain = individual_share * role_multiplier
            self.energy_level = min(100, self.energy_level + energy_gain)
            self.happiness_level = min(100, self.happiness_level + 20)
            self.is_hungry = False
            
            self._log_activity("群体狩猎", f"群体成功捕获{prey_type}({prey_size})")
            
            return {
                **hunt_result,
                'energy_gained': round(energy_gain, 1),
                'pack_role': self.pack_behavior.pack_role,
                'sharing_ratio': f"{role_multiplier:.1f}x"
            }
        else:
            # 狩猎失败
            self.energy_level = max(0, self.energy_level - 20)
            self.happiness_level = max(0, self.happiness_level - 10)
            
            return hunt_result
    
    def get_life_expectancy(self) -> int:
        """获取预期寿命（重写父类方法）"""
        # 犬科动物寿命主要取决于体重
        if self.weight < 10:
            return random.randint(12, 16)  # 小型犬科动物
        elif self.weight < 30:
            return random.randint(10, 14)  # 中型犬科动物
        else:
            return random.randint(8, 12)   # 大型犬科动物
    
    def make_sound(self) -> str:
        """发出声音（重写父类方法）"""
        # 根据情况选择合适的声音
        if self.pack_behavior.pack_members and random.random() < 0.3:
            return self.communication.howl()['sound_type']
        elif self.happiness_level > 70:
            return self.communication.bark('轻微', '问候')['sound_type']
        elif self.energy_level < 30:
            return "呜咽"
        else:
            return self.communication.bark()['sound_type']
    
    def get_canine_specific_info(self) -> Dict[str, Any]:
        """获取犬科动物特有信息"""
        return {
            'bite_force_psi': self.bite_force_psi,
            'pack_instinct': self.pack_instinct,
            'tail_length_cm': self.tail_length_cm,
            'ear_type': self.ear_type,
            'snout_length_cm': self.snout_length_cm,
            'loyalty_level': self.loyalty_level,
            'territorial_instinct': self.territorial_instinct,
            'hunting_drive': self.hunting_drive,
            'playfulness': self.playfulness,
            'trainability_score': self.trainability_score,
            'scent_tracking_ability': self.scent_tracking_ability,
            'pack_role': self.pack_behavior.pack_role,
            'pack_size': len(self.pack_behavior.pack_members),
            'learned_commands_count': len(self.learned_commands),
            'buried_items_count': len([item for item in self.buried_items if item['retrieval_date'] is None]),
            'vocal_repertoire': self.communication.vocal_repertoire,
            'tracking_success_rate': len([r for r in self.tracking_records if 'success' in r.record_type]) / max(1, len(self.tracking_records))
        }
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """获取详细状态信息（重写父类方法）"""
        base_status = super().get_detailed_status()
        canine_info = self.get_canine_specific_info()
        
        return {
            **base_status,
            'canine_specific': canine_info,
            'pack_behavior': {
                'role': self.pack_behavior.pack_role,
                'dominance_level': self.pack_behavior.dominance_level,
                'pack_members': len(self.pack_behavior.pack_members),
                'territorial_markings': len(self.pack_behavior.territorial_markings),
                'hunting_contributions': self.pack_behavior.hunting_contributions
            },
            'communication_abilities': {
                'vocal_sounds': len(self.communication.vocal_repertoire),
                'hearing_acuity': self.communication.hearing_acuity,
                'recent_communications': len(self.communication.communication_records)
            },
            'training_progress': {
                'commands_known': self.learned_commands,
                'training_sessions': len(self.training_sessions),
                'obedience_rate': self.loyalty_level
            }
        }
    
    @classmethod
    def get_canine_statistics(cls) -> Dict[str, Any]:
        """获取犬科动物统计信息"""
        mammal_stats = cls.get_mammal_statistics()
        return {
            **mammal_stats,
            'canine_count': cls.canine_count,
            'pack_formation_threshold': cls.pack_formation_threshold
        }
    
    def __str__(self) -> str:
        pack_info = f"({self.pack_behavior.pack_role})" if self.pack_behavior.pack_members else "(独行)"
        return f"犬科动物 - {self.species} - {self.name} {pack_info}"


# 犬科动物专用工具函数
def simulate_pack_dynamics(canines: List[Canine]) -> Dict[str, Any]:
    """模拟群体动态"""
    if len(canines) < 2:
        return {'status': 'insufficient_pack_size', 'message': '需要至少2只犬科动物'}
    
    pack_canines = [c for c in canines if c.pack_behavior.pack_members and c.is_alive]
    
    if not pack_canines:
        return {'status': 'no_pack_members', 'message': '没有群体成员'}
    
    # 分析群体结构
    roles = {}
    for canine in pack_canines:
        role = canine.pack_behavior.pack_role
        roles[role] = roles.get(role, 0) + 1
    
    # 计算群体凝聚力
    avg_loyalty = sum(c.loyalty_level for c in pack_canines) / len(pack_canines)
    avg_dominance = sum(c.pack_behavior.dominance_level for c in pack_canines) / len(pack_canines)
    
    # 群体健康度
    pack_health = {
        'cohesion': avg_loyalty,
        'hierarchy_stability': 100 - abs(avg_dominance - 50),  # 50为理想的平衡点
        'size': len(pack_canines),
        'role_distribution': roles
    }
    
    return {
        'status': 'success',
        'pack_analysis': pack_health,
        'recommendations': _generate_pack_recommendations(pack_health)
    }


def _generate_pack_recommendations(pack_health: Dict[str, Any]) -> List[str]:
    """生成群体管理建议"""
    recommendations = []
    
    if pack_health['cohesion'] < 60:
        recommendations.append("增加群体活动以提高凝聚力")
    
    if pack_health['hierarchy_stability'] < 70:
        recommendations.append("需要建立更清晰的等级制度")
    
    if pack_health['size'] > 8:
        recommendations.append("考虑分割群体以提高管理效率")
    elif pack_health['size'] < 3:
        recommendations.append("考虑增加群体成员")
    
    role_dist = pack_health['role_distribution']
    if role_dist.get('首领', 0) > 1:
        recommendations.append("存在多个首领，需要解决领导权冲突")
    elif role_dist.get('首领', 0) == 0:
        recommendations.append("群体缺乏领导者")
    
    return recommendations


def train_canine_group(canines: List[Canine], commands: List[str], trainer: str = "训练师") -> Dict[str, Any]:
    """批量训练犬科动物"""
    results = []
    
    for canine in canines:
        if not canine.is_alive:
            continue
        
        canine_results = []
        for command in commands:
            result = canine.learn_command(command, trainer, random.randint(8, 15))
            canine_results.append(result)
        
        success_rate = len([r for r in canine_results if r['status'] == 'success']) / len(commands)
        
        results.append({
            'canine': canine.get_basic_info(),
            'training_results': canine_results,
            'success_rate': round(success_rate, 2),
            'trainability': canine.trainability_score
        })
    
    return {
        'training_session': {
            'trainer': trainer,
            'commands_taught': commands,
            'participants': len(results),
            'individual_results': results
        }
    }


def organize_pack_hunt(pack_canines: List[Canine], target_prey: str) -> Dict[str, Any]:
    """组织群体狩猎活动"""
    if not pack_canines:
        return {'status': 'error', 'message': '没有群体成员'}
    
    # 选择首领协调狩猎
    alpha = None
    for canine in pack_canines:
        if canine.pack_behavior.pack_role == "首领":
            alpha = canine
            break
    
    if not alpha:
        return {'status': 'no_leader', 'message': '群体缺乏首领'}
    
    # 执行群体狩猎
    hunt_results = []
    for canine in pack_canines:
        result = canine.hunt_as_pack(target_prey)
        hunt_results.append({
            'canine': canine.get_basic_info(),
            'hunt_result': result
        })
    
    # 计算整体成功率
    successful_hunts = len([r for r in hunt_results if r['hunt_result']['status'] == 'success'])
    success_rate = successful_hunts / len(pack_canines)
    
    return {
        'hunt_coordination': {
            'alpha_leader': alpha.get_basic_info(),
            'target_prey': target_prey,
            'pack_size': len(pack_canines),
            'success_rate': round(success_rate, 2),
            'individual_results': hunt_results
        }
    }