"""
哺乳动物类模块
继承自Animal基类，添加哺乳动物特有的属性和行为
"""

import datetime
from typing import Optional, List, Dict, Any, Tuple
import random
import math
from animal import Animal, AnimalRecord


class MammalBreeding:
    """哺乳动物繁殖管理类"""
    
    def __init__(self):
        self.is_fertile = True
        self.mating_season: Optional[Tuple[int, int]] = None  # (开始月份, 结束月份)
        self.gestation_period_days = 0
        self.offspring_history: List[Dict[str, Any]] = []
        self.breeding_records: List[AnimalRecord] = []
        self.last_mating_attempt: Optional[datetime.datetime] = None
    
    def set_mating_season(self, start_month: int, end_month: int):
        """设置交配季节"""
        if 1 <= start_month <= 12 and 1 <= end_month <= 12:
            self.mating_season = (start_month, end_month)
        else:
            raise ValueError("月份必须在1-12之间")
    
    def is_mating_season(self) -> bool:
        """检查是否为交配季节"""
        if not self.mating_season:
            return True  # 如果没有设置季节限制，则全年可繁殖
        
        current_month = datetime.datetime.now().month
        start, end = self.mating_season
        
        if start <= end:
            return start <= current_month <= end
        else:  # 跨年的情况，如11月到2月
            return current_month >= start or current_month <= end
    
    def attempt_mating(self, partner_info: Dict[str, Any]) -> Dict[str, Any]:
        """尝试交配"""
        if not self.is_fertile:
            return {'success': False, 'reason': '不具备繁殖能力'}
        
        if not self.is_mating_season():
            return {'success': False, 'reason': '不在交配季节'}
        
        # 检查上次交配时间间隔
        if self.last_mating_attempt:
            days_since_last = (datetime.datetime.now() - self.last_mating_attempt).days
            if days_since_last < 30:
                return {'success': False, 'reason': '距离上次交配时间太短'}
        
        # 模拟交配成功率
        success_rate = 0.7  # 70%的基础成功率
        if random.random() <= success_rate:
            self.last_mating_attempt = datetime.datetime.now()
            expected_birth = datetime.datetime.now() + datetime.timedelta(days=self.gestation_period_days)
            
            record = AnimalRecord('mating', f"与{partner_info.get('name', '未知')}交配成功")
            self.breeding_records.append(record)
            
            return {
                'success': True,
                'expected_birth_date': expected_birth,
                'gestation_period_days': self.gestation_period_days
            }
        else:
            return {'success': False, 'reason': '交配未成功'}
    
    def give_birth(self, offspring_count: int = 1) -> Dict[str, Any]:
        """分娩"""
        birth_info = {
            'birth_date': datetime.datetime.now(),
            'offspring_count': offspring_count,
            'birth_weight_total': random.uniform(0.5, 2.0) * offspring_count,
            'complications': random.choice([None, None, None, '轻微并发症'])  # 25%概率有轻微并发症
        }
        
        self.offspring_history.append(birth_info)
        
        record = AnimalRecord('birth', f"成功分娩{offspring_count}只幼崽")
        self.breeding_records.append(record)
        
        return birth_info


class MammalNutrition:
    """哺乳动物营养管理类"""
    
    def __init__(self):
        self.is_lactating = False
        self.lactation_start: Optional[datetime.datetime] = None
        self.milk_production_rate = 0.0  # 升/天
        self.dietary_preferences: List[str] = []
        self.food_allergies: List[str] = []
        self.supplement_needs: Dict[str, float] = {}
        self.feeding_schedule: List[Dict[str, Any]] = []
        self.nutrition_records: List[AnimalRecord] = []
    
    def start_lactation(self, milk_production_rate: float = 1.0):
        """开始哺乳期"""
        self.is_lactating = True
        self.lactation_start = datetime.datetime.now()
        self.milk_production_rate = milk_production_rate
        
        record = AnimalRecord('lactation_start', f"开始哺乳期，产奶率{milk_production_rate}升/天")
        self.nutrition_records.append(record)
    
    def stop_lactation(self):
        """结束哺乳期"""
        if self.is_lactating:
            duration = (datetime.datetime.now() - self.lactation_start).days
            self.is_lactating = False
            self.milk_production_rate = 0.0
            
            record = AnimalRecord('lactation_end', f"哺乳期结束，持续{duration}天")
            self.nutrition_records.append(record)
    
    def calculate_caloric_needs(self, base_weight: float, activity_level: str = 'moderate') -> Dict[str, float]:
        """计算卡路里需求"""
        # 基础代谢率 (BMR)
        bmr = 70 * (base_weight ** 0.75)  # 使用Kleiber定律
        
        # 活动系数
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        daily_calories = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # 哺乳期额外需求
        if self.is_lactating:
            lactation_calories = self.milk_production_rate * 500  # 每升奶约需500卡路里
            daily_calories += lactation_calories
        
        return {
            'bmr': round(bmr, 2),
            'daily_needs': round(daily_calories, 2),
            'lactation_extra': round(self.milk_production_rate * 500, 2) if self.is_lactating else 0
        }
    
    def add_dietary_preference(self, food_type: str):
        """添加饮食偏好"""
        if food_type not in self.dietary_preferences:
            self.dietary_preferences.append(food_type)
    
    def add_food_allergy(self, allergen: str):
        """添加食物过敏"""
        if allergen not in self.food_allergies:
            self.food_allergies.append(allergen)
            record = AnimalRecord('allergy_discovered', f"发现对{allergen}过敏")
            self.nutrition_records.append(record)
    
    def create_feeding_plan(self, weight: float, age: int) -> List[Dict[str, Any]]:
        """创建喂食计划"""
        caloric_needs = self.calculate_caloric_needs(weight)
        daily_calories = caloric_needs['daily_needs']
        
        # 根据年龄调整喂食频次
        if age < 1:  # 幼崽
            meal_count = 6
        elif age < 3:  # 青少年
            meal_count = 4
        else:  # 成年
            meal_count = 2
        
        calories_per_meal = daily_calories / meal_count
        
        feeding_times = []
        hour_interval = 24 // meal_count
        
        for i in range(meal_count):
            hour = (6 + i * hour_interval) % 24
            feeding_times.append({
                'time': f"{hour:02d}:00",
                'calories': round(calories_per_meal, 2),
                'portion_description': self._get_portion_description(calories_per_meal)
            })
        
        self.feeding_schedule = feeding_times
        return feeding_times
    
    def _get_portion_description(self, calories: float) -> str:
        """获取食物分量描述"""
        if calories < 200:
            return "小份"
        elif calories < 500:
            return "中份"
        elif calories < 1000:
            return "大份"
        else:
            return "超大份"


class Mammal(Animal):
    """
    哺乳动物类
    继承自Animal基类，添加哺乳动物特有的属性和行为
    """
    
    # 类变量
    mammal_count = 0
    body_temperature_range = (36.0, 39.0)  # 正常体温范围
    
    def __init__(self, name: str, species: str, age: int, weight: float,
                 owner: str = "未知", gender: str = "未知", 
                 fur_color: str = "棕色", fur_type: str = "短毛"):
        # 调用父类构造函数
        super().__init__(name, species, age, weight, owner, gender)
        
        # 哺乳动物特有属性
        self.fur_color = fur_color
        self.fur_type = fur_type
        self.body_temperature = random.uniform(*self.body_temperature_range)
        self.is_warm_blooded = True
        self.has_mammary_glands = True
        
        # 生理特征
        self.milk_teeth_count = self._calculate_milk_teeth()
        self.adult_teeth_count = self._calculate_adult_teeth()
        self.current_teeth_count = self.milk_teeth_count if age < 1 else self.adult_teeth_count
        
        # 行为特征
        self.is_nocturnal = False
        self.social_behavior = "群居"  # 群居, 独居, 成对
        self.territoriality = "中等"   # 低, 中等, 高
        self.migration_pattern = "无"  # 无, 季节性, 不规律
        
        # 繁殖和营养管理
        self.breeding = MammalBreeding()
        self.nutrition = MammalNutrition()
        
        # 季节适应性
        self.seasonal_coat_change = False
        self.hibernation_capable = False
        self.winter_weight_gain = 0.0
        
        # 感官能力
        self.hearing_range_hz = (20, 20000)  # 听觉范围
        self.vision_type = "彩色"  # 彩色, 单色, 夜视
        self.smell_sensitivity = "高"  # 低, 中, 高
        
        # 运动能力
        self.max_speed_kmh = 0.0
        self.climbing_ability = "无"  # 无, 低, 中, 高
        self.swimming_ability = "无"  # 无, 低, 中, 高
        self.jumping_height_m = 0.0
        
        # 环境适应
        self.temperature_tolerance = (-10, 35)  # 温度耐受范围
        self.altitude_tolerance_m = 3000
        self.water_dependency = "中等"  # 低, 中等, 高
        
        # 更新计数
        Mammal.mammal_count += 1
        
        # 记录哺乳动物特有信息
        self._log_activity("哺乳动物创建", f"哺乳动物{self.name}已注册，毛色: {self.fur_color}")
    
    def _calculate_milk_teeth(self) -> int:
        """计算乳牙数量"""
        # 根据物种大致估算，可以在子类中重写
        base_teeth = 28
        size_factor = min(self.weight / 50, 2.0)  # 体重影响因子
        return int(base_teeth * size_factor)
    
    def _calculate_adult_teeth(self) -> int:
        """计算成年牙齿数量"""
        return int(self._calculate_milk_teeth() * 1.2)
    
    def regulate_body_temperature(self, ambient_temp: float) -> Dict[str, Any]:
        """调节体温"""
        if not self.is_alive:
            return {'status': 'error', 'message': '动物已死亡'}
        
        temp_diff = abs(self.body_temperature - ambient_temp)
        energy_cost = 0
        
        if ambient_temp < self.temperature_tolerance[0]:
            # 太冷，需要产热
            self.body_temperature = min(self.body_temperature_range[1], 
                                      self.body_temperature + 0.5)
            energy_cost = temp_diff * 2
            mechanism = "颤抖产热, 血管收缩"
            
        elif ambient_temp > self.temperature_tolerance[1]:
            # 太热，需要散热
            self.body_temperature = max(self.body_temperature_range[0], 
                                      self.body_temperature - 0.3)
            energy_cost = temp_diff * 1.5
            mechanism = "流汗散热, 血管扩张, 喘息"
            
        else:
            # 温度适宜
            target_temp = sum(self.body_temperature_range) / 2
            self.body_temperature += (target_temp - self.body_temperature) * 0.1
            mechanism = "正常代谢维持"
        
        # 消耗能量
        self.energy_level = max(0, self.energy_level - energy_cost)
        
        self._log_activity("体温调节", f"环境温度{ambient_temp}°C，体温调节至{self.body_temperature:.1f}°C")
        
        return {
            'status': 'success',
            'current_temperature': round(self.body_temperature, 1),
            'mechanism': mechanism,
            'energy_cost': round(energy_cost, 1),
            'comfort_level': 'comfortable' if self.temperature_tolerance[0] <= ambient_temp <= self.temperature_tolerance[1] else 'stressed'
        }
    
    def groom_fur(self, duration_minutes: int = 15):
        """梳理毛发"""
        if not self.is_alive:
            return
        
        # 梳理毛发提升快乐度和健康
        self.happiness_level = min(100, self.happiness_level + 8)
        self.energy_level = max(0, self.energy_level - 5)
        
        # 改善毛发状态
        if hasattr(self, 'fur_condition'):
            self.fur_condition = min(100, getattr(self, 'fur_condition', 80) + 10)
        else:
            self.fur_condition = 90
        
        self._log_activity("梳理", f"梳理毛发{duration_minutes}分钟，毛发状态改善")
    
    def shed_fur(self, season: str = "春季"):
        """换毛"""
        if not self.seasonal_coat_change:
            return
        
        fur_shed_amount = random.uniform(0.1, 0.3)  # 脱毛比例
        
        # 根据季节调整毛发类型
        if season in ["秋季", "冬季"]:
            self.fur_type = "厚毛" if "薄" not in self.fur_type else "中等毛"
        else:
            self.fur_type = "薄毛" if "厚" not in self.fur_type else "中等毛"
        
        self._log_activity("换毛", f"{season}换毛，脱毛量{fur_shed_amount:.1%}")
    
    def nurse_offspring(self, offspring_count: int = 1) -> Dict[str, Any]:
        """哺育幼崽"""
        if not self.nutrition.is_lactating:
            return {'status': 'error', 'message': '不在哺乳期'}
        
        if self.gender != "雌性":
            return {'status': 'error', 'message': '只有雌性可以哺乳'}
        
        # 计算哺乳消耗
        milk_needed = offspring_count * 0.2  # 每只幼崽需要0.2升奶
        energy_cost = milk_needed * 30  # 每升奶消耗30点能量
        
        if self.energy_level < energy_cost:
            return {'status': 'insufficient_energy', 'message': '能量不足，无法充分哺乳'}
        
        self.energy_level -= energy_cost
        self.happiness_level = min(100, self.happiness_level + 15)  # 哺育增加快乐度
        
        # 额外营养需求
        caloric_needs = self.nutrition.calculate_caloric_needs(self.weight)
        
        self._log_activity("哺育", f"哺育{offspring_count}只幼崽，消耗能量{energy_cost}")
        
        return {
            'status': 'success',
            'milk_produced': round(milk_needed, 2),
            'energy_consumed': energy_cost,
            'additional_caloric_needs': caloric_needs['lactation_extra']
        }
    
    def establish_territory(self, territory_size_sqm: float) -> Dict[str, Any]:
        """建立领地"""
        if self.territoriality == "低":
            return {'status': 'not_applicable', 'message': '该物种领地意识较弱'}
        
        # 根据体重和社交行为计算合理的领地大小
        optimal_size = self.weight * 100  # 基础领地大小
        
        if self.social_behavior == "独居":
            optimal_size *= 2
        elif self.social_behavior == "群居":
            optimal_size *= 0.5
        
        territory_quality = min(100, (territory_size_sqm / optimal_size) * 100)
        
        # 建立领地影响快乐度
        happiness_change = (territory_quality - 50) * 0.3
        self.happiness_level = max(0, min(100, self.happiness_level + happiness_change))
        
        self._log_activity("领地", f"建立{territory_size_sqm:.0f}平方米领地")
        
        return {
            'status': 'success',
            'territory_size': territory_size_sqm,
            'optimal_size': round(optimal_size, 0),
            'quality_score': round(territory_quality, 1),
            'happiness_impact': round(happiness_change, 1)
        }
    
    def hunt_prey(self, prey_type: str, success_rate: float = 0.6) -> Dict[str, Any]:
        """狩猎猎物"""
        if self.energy_level < 30:
            return {'status': 'insufficient_energy', 'message': '能量不足，无法狩猎'}
        
        # 狩猎消耗能量
        hunting_energy_cost = 25
        self.energy_level -= hunting_energy_cost
        
        # 根据成功率决定狩猎结果
        if random.random() <= success_rate:
            # 狩猎成功
            prey_energy_gain = random.uniform(40, 60)
            self.energy_level = min(100, self.energy_level + prey_energy_gain)
            self.happiness_level = min(100, self.happiness_level + 20)
            self.is_hungry = False
            
            self._log_activity("狩猎", f"成功捕获{prey_type}")
            
            return {
                'status': 'success',
                'prey_caught': prey_type,
                'energy_gained': round(prey_energy_gain, 1),
                'net_energy_change': round(prey_energy_gain - hunting_energy_cost, 1)
            }
        else:
            # 狩猎失败
            self.happiness_level = max(0, self.happiness_level - 10)
            
            self._log_activity("狩猎", f"尝试捕获{prey_type}失败")
            
            return {
                'status': 'failed',
                'energy_lost': hunting_energy_cost,
                'prey_escaped': prey_type
            }
    
    def migrate(self, destination: str, distance_km: float) -> Dict[str, Any]:
        """迁徙"""
        if self.migration_pattern == "无":
            return {'status': 'not_applicable', 'message': '该物种不进行迁徙'}
        
        # 计算迁徙消耗
        migration_energy_cost = distance_km * 0.5
        migration_time_days = distance_km / (self.max_speed_kmh * 8)  # 假设每天行进8小时
        
        if self.energy_level < migration_energy_cost:
            return {'status': 'insufficient_energy', 'message': '能量不足，无法完成迁徙'}
        
        self.energy_level -= migration_energy_cost
        
        # 迁徙成功后的好处
        self.happiness_level = min(100, self.happiness_level + 25)
        
        self._log_activity("迁徙", f"迁徙到{destination}，距离{distance_km}公里")
        
        return {
            'status': 'success',
            'destination': destination,
            'distance_traveled': distance_km,
            'energy_consumed': migration_energy_cost,
            'estimated_travel_time_days': round(migration_time_days, 1)
        }
    
    def prepare_for_hibernation(self) -> Dict[str, Any]:
        """准备冬眠"""
        if not self.hibernation_capable:
            return {'status': 'not_applicable', 'message': '该物种不具备冬眠能力'}
        
        # 冬眠前增重
        weight_gain = self.weight * 0.3  # 增重30%
        self.weight += weight_gain
        self.winter_weight_gain = weight_gain
        
        # 降低代谢率
        self.energy_level = 95  # 保存能量
        
        self._log_activity("冬眠准备", f"为冬眠增重{weight_gain:.1f}公斤")
        
        return {
            'status': 'ready',
            'weight_gained': round(weight_gain, 1),
            'new_weight': round(self.weight, 1),
            'energy_stored': 95
        }
    
    def get_life_expectancy(self) -> int:
        """获取预期寿命（重写父类抽象方法）"""
        # 哺乳动物的平均寿命，可以在具体子类中进一步细化
        base_lifespan = 15
        
        # 根据体重调整寿命
        if self.weight < 5:
            return base_lifespan - 5  # 小型哺乳动物寿命较短
        elif self.weight > 100:
            return base_lifespan + 10  # 大型哺乳动物寿命较长
        else:
            return base_lifespan
    
    def make_sound(self) -> str:
        """发出声音（重写父类抽象方法）"""
        # 基础哺乳动物叫声，子类可以重写为更具体的声音
        sounds = ["呜呜", "嗷嗷", "啾啾", "咕噜"]
        return random.choice(sounds)
    
    def get_mammal_specific_info(self) -> Dict[str, Any]:
        """获取哺乳动物特有信息"""
        return {
            'fur_color': self.fur_color,
            'fur_type': self.fur_type,
            'body_temperature': round(self.body_temperature, 1),
            'teeth_count': self.current_teeth_count,
            'social_behavior': self.social_behavior,
            'territoriality': self.territoriality,
            'hibernation_capable': self.hibernation_capable,
            'max_speed_kmh': self.max_speed_kmh,
            'climbing_ability': self.climbing_ability,
            'swimming_ability': self.swimming_ability,
            'is_lactating': self.nutrition.is_lactating,
            'milk_production_rate': self.nutrition.milk_production_rate,
            'breeding_season': self.breeding.mating_season,
            'offspring_count': len(self.breeding.offspring_history)
        }
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """获取详细状态信息（重写父类方法）"""
        base_status = super().get_detailed_status()
        mammal_info = self.get_mammal_specific_info()
        
        return {
            **base_status,
            'mammal_specific': mammal_info,
            'caloric_needs': self.nutrition.calculate_caloric_needs(self.weight),
            'feeding_schedule': self.nutrition.feeding_schedule,
            'temperature_regulation': {
                'current_temp': round(self.body_temperature, 1),
                'normal_range': self.body_temperature_range,
                'tolerance_range': self.temperature_tolerance
            }
        }
    
    @classmethod
    def get_mammal_statistics(cls) -> Dict[str, Any]:
        """获取哺乳动物统计信息"""
        base_stats = cls.get_species_statistics()
        return {
            **base_stats,
            'mammal_count': cls.mammal_count,
            'body_temperature_range': cls.body_temperature_range
        }
    
    def __str__(self) -> str:
        return f"哺乳动物 - {self.species} - {self.name} ({self.fur_color}{self.fur_type})"


# 哺乳动物工具函数
def create_breeding_pair(male: Mammal, female: Mammal) -> Dict[str, Any]:
    """创建繁殖配对"""
    if male.gender != "雄性" or female.gender != "雌性":
        return {'status': 'error', 'message': '性别不匹配'}
    
    if male.species != female.species:
        return {'status': 'error', 'message': '物种不匹配'}
    
    # 尝试交配
    partner_info = {'name': male.name, 'id': male.animal_id}
    mating_result = female.breeding.attempt_mating(partner_info)
    
    return {
        'pair': {'male': male.get_basic_info(), 'female': female.get_basic_info()},
        'mating_result': mating_result
    }


def calculate_pack_hierarchy(mammals: List[Mammal]) -> List[Dict[str, Any]]:
    """计算群体等级制度"""
    if not mammals:
        return []
    
    # 根据年龄、体重、快乐度等因素计算等级
    hierarchy = []
    for mammal in mammals:
        if mammal.social_behavior == "群居":
            dominance_score = (
                mammal.age * 2 +
                mammal.weight * 0.5 +
                mammal.happiness_level * 0.3 +
                mammal.energy_level * 0.2
            )
            
            hierarchy.append({
                'animal': mammal.get_basic_info(),
                'dominance_score': round(dominance_score, 1),
                'social_role': 'alpha' if dominance_score > 150 else 
                              'beta' if dominance_score > 100 else 'omega'
            })
    
    # 按支配分数排序
    hierarchy.sort(key=lambda x: x['dominance_score'], reverse=True)
    
    # 分配等级
    for i, member in enumerate(hierarchy):
        member['rank'] = i + 1
    
    return hierarchy


def simulate_seasonal_changes(mammals: List[Mammal], season: str) -> List[Dict[str, Any]]:
    """模拟季节变化对哺乳动物的影响"""
    results = []
    
    seasonal_effects = {
        '春季': {'temperature': 15, 'food_availability': 0.8, 'breeding_boost': True},
        '夏季': {'temperature': 25, 'food_availability': 1.0, 'breeding_boost': False},
        '秋季': {'temperature': 10, 'food_availability': 0.9, 'breeding_boost': False},
        '冬季': {'temperature': -5, 'food_availability': 0.4, 'breeding_boost': False}
    }
    
    effects = seasonal_effects.get(season, seasonal_effects['春季'])
    
    for mammal in mammals:
        if not mammal.is_alive:
            continue
        
        # 体温调节
        temp_regulation = mammal.regulate_body_temperature(effects['temperature'])
        
        # 换毛
        if mammal.seasonal_coat_change:
            mammal.shed_fur(season)
        
        # 食物可获得性影响
        food_impact = effects['food_availability']
        if food_impact < 0.6:
            mammal.energy_level = max(20, mammal.energy_level * food_impact)
        
        # 繁殖季节影响
        if effects['breeding_boost'] and mammal.breeding.is_mating_season():
            mammal.happiness_level = min(100, mammal.happiness_level + 10)
        
        results.append({
            'animal': mammal.get_basic_info(),
            'seasonal_effects': {
                'temperature_regulation': temp_regulation,
                'food_availability_impact': food_impact,
                'breeding_season_active': effects['breeding_boost'] and mammal.breeding.is_mating_season()
            }
        })
    
    return results