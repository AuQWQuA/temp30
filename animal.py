"""
动物基类模块
包含所有动物的基本属性和行为
"""

import datetime
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import json


class AnimalRecord:
    """动物记录类，用于存储动物的历史信息"""
    
    def __init__(self, record_type: str, description: str, timestamp: Optional[datetime.datetime] = None):
        self.record_type = record_type
        self.description = description
        self.timestamp = timestamp or datetime.datetime.now()
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成唯一记录ID"""
        return f"{self.record_type}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'id': self.id,
            'type': self.record_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __str__(self) -> str:
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.record_type}: {self.description}"


class AnimalHealth:
    """动物健康状态管理类"""
    
    def __init__(self):
        self.vaccinations: List[Dict[str, Any]] = []
        self.medical_records: List[AnimalRecord] = []
        self.health_status = "良好"
        self.last_checkup: Optional[datetime.datetime] = None
        self.allergies: List[str] = []
        self.medications: List[Dict[str, Any]] = []
    
    def add_vaccination(self, vaccine_name: str, date: datetime.datetime, next_due: Optional[datetime.datetime] = None):
        """添加疫苗接种记录"""
        vaccination = {
            'vaccine': vaccine_name,
            'date': date,
            'next_due': next_due,
            'administered_by': 'veterinarian'
        }
        self.vaccinations.append(vaccination)
        self.add_medical_record('vaccination', f"接种{vaccine_name}疫苗")
    
    def add_medical_record(self, record_type: str, description: str):
        """添加医疗记录"""
        record = AnimalRecord(record_type, description)
        self.medical_records.append(record)
    
    def update_health_status(self, status: str, notes: str = ""):
        """更新健康状态"""
        self.health_status = status
        self.last_checkup = datetime.datetime.now()
        if notes:
            self.add_medical_record('checkup', f"健康状态更新为{status}: {notes}")
    
    def add_allergy(self, allergy: str):
        """添加过敏信息"""
        if allergy not in self.allergies:
            self.allergies.append(allergy)
            self.add_medical_record('allergy', f"发现过敏源: {allergy}")
    
    def is_vaccination_due(self, vaccine_name: str) -> bool:
        """检查是否需要接种疫苗"""
        for vaccination in self.vaccinations:
            if vaccination['vaccine'] == vaccine_name and vaccination.get('next_due'):
                return datetime.datetime.now() >= vaccination['next_due']
        return True
    
    def get_health_summary(self) -> Dict[str, Any]:
        """获取健康状况摘要"""
        return {
            'status': self.health_status,
            'last_checkup': self.last_checkup.isoformat() if self.last_checkup else None,
            'vaccination_count': len(self.vaccinations),
            'medical_records_count': len(self.medical_records),
            'allergies_count': len(self.allergies),
            'medications_count': len(self.medications)
        }


class Animal(ABC):
    """
    动物基类
    包含所有动物的基本属性和行为
    """
    
    # 类变量
    total_animals = 0
    species_registry: Dict[str, int] = {}
    
    def __init__(self, name: str, species: str, age: int, weight: float, 
                 owner: str = "未知", gender: str = "未知"):
        # 基本信息
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight
        self.owner = owner
        self.gender = gender
        
        # 唯一标识
        self.animal_id = self._generate_animal_id()
        
        # 状态信息
        self.is_alive = True
        self.is_hungry = False
        self.is_sleeping = False
        self.energy_level = 100
        self.happiness_level = 80
        
        # 时间信息
        self.birth_date = datetime.datetime.now() - datetime.timedelta(days=age*365)
        self.registration_date = datetime.datetime.now()
        self.last_fed = None
        self.last_exercise = None
        
        # 健康管理
        self.health = AnimalHealth()
        
        # 行为记录
        self.activity_log: List[AnimalRecord] = []
        self.favorite_activities: List[str] = []
        
        # 更新类统计
        Animal.total_animals += 1
        Animal.species_registry[species] = Animal.species_registry.get(species, 0) + 1
        
        # 记录创建日志
        self._log_activity("创建", f"动物{self.name}已注册到系统")
    
    def _generate_animal_id(self) -> str:
        """生成唯一的动物ID"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{self.species[:3].upper()}{timestamp}{Animal.total_animals:04d}"
    
    def _log_activity(self, activity_type: str, description: str):
        """记录活动日志"""
        record = AnimalRecord(activity_type, description)
        self.activity_log.append(record)
    
    def feed(self, food_type: str = "普通食物", amount: float = 1.0):
        """喂食动物"""
        if not self.is_alive:
            raise ValueError(f"{self.name}已经死亡，无法喂食")
        
        self.is_hungry = False
        self.energy_level = min(100, self.energy_level + 20)
        self.happiness_level = min(100, self.happiness_level + 10)
        self.last_fed = datetime.datetime.now()
        
        self._log_activity("喂食", f"喂食{food_type}，数量: {amount}")
    
    def exercise(self, exercise_type: str = "散步", duration: int = 30):
        """让动物运动"""
        if not self.is_alive:
            raise ValueError(f"{self.name}已经死亡，无法运动")
        
        if self.energy_level < 20:
            raise ValueError(f"{self.name}太累了，需要休息")
        
        self.energy_level = max(0, self.energy_level - 15)
        self.happiness_level = min(100, self.happiness_level + 15)
        self.last_exercise = datetime.datetime.now()
        
        if exercise_type not in self.favorite_activities:
            self.favorite_activities.append(exercise_type)
        
        self._log_activity("运动", f"进行{exercise_type}运动，持续{duration}分钟")
    
    def sleep(self, duration: int = 8):
        """让动物睡觉"""
        if not self.is_alive:
            return
        
        self.is_sleeping = True
        self.energy_level = min(100, self.energy_level + duration * 5)
        
        self._log_activity("休息", f"睡觉{duration}小时")
        
        # 模拟睡觉过程
        import time
        time.sleep(0.1)  # 模拟时间流逝
        self.is_sleeping = False
    
    def age_up(self, years: int = 1):
        """动物年龄增长"""
        if not self.is_alive:
            return
        
        old_age = self.age
        self.age += years
        
        # 年龄增长可能影响健康
        if self.age > self.get_life_expectancy() * 0.8:
            self.health.update_health_status("老年", "进入老年阶段，需要更多关注")
        
        self._log_activity("成长", f"从{old_age}岁成长到{self.age}岁")
    
    def get_age_in_human_years(self) -> int:
        """获取相当于人类年龄的岁数"""
        # 默认计算方式，子类可以重写
        return self.age * 7
    
    @abstractmethod
    def get_life_expectancy(self) -> int:
        """获取预期寿命（抽象方法，子类必须实现）"""
        pass
    
    @abstractmethod
    def make_sound(self) -> str:
        """发出声音（抽象方法，子类必须实现）"""
        pass
    
    def get_basic_info(self) -> Dict[str, Any]:
        """获取基本信息"""
        return {
            'id': self.animal_id,
            'name': self.name,
            'species': self.species,
            'age': self.age,
            'weight': self.weight,
            'owner': self.owner,
            'gender': self.gender,
            'is_alive': self.is_alive,
            'energy_level': self.energy_level,
            'happiness_level': self.happiness_level
        }
    
    def get_detailed_status(self) -> Dict[str, Any]:
        """获取详细状态信息"""
        return {
            **self.get_basic_info(),
            'birth_date': self.birth_date.isoformat(),
            'registration_date': self.registration_date.isoformat(),
            'last_fed': self.last_fed.isoformat() if self.last_fed else None,
            'last_exercise': self.last_exercise.isoformat() if self.last_exercise else None,
            'health_summary': self.health.get_health_summary(),
            'activity_count': len(self.activity_log),
            'favorite_activities': self.favorite_activities,
            'human_age_equivalent': self.get_age_in_human_years(),
            'life_expectancy': self.get_life_expectancy()
        }
    
    def export_to_json(self, filename: Optional[str] = None) -> str:
        """导出动物信息到JSON文件"""
        data = self.get_detailed_status()
        
        if filename is None:
            filename = f"{self.animal_id}_{self.name}_profile.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return f"动物信息已导出到 {filename}"
        except Exception as e:
            return f"导出失败: {str(e)}"
    
    def calculate_daily_needs(self) -> Dict[str, Any]:
        """计算每日需求"""
        base_food = self.weight * 0.03  # 体重的3%
        base_water = self.weight * 0.1   # 体重的10%
        base_exercise = 30 + (self.age * 2)  # 基础运动时间
        
        return {
            'food_kg': round(base_food, 2),
            'water_liters': round(base_water, 2),
            'exercise_minutes': min(base_exercise, 120),
            'sleep_hours': 8 + (max(0, 15 - self.age) * 0.5)
        }
    
    def check_wellness(self) -> Dict[str, Any]:
        """检查动物福利状况"""
        issues = []
        recommendations = []
        
        # 检查能量水平
        if self.energy_level < 30:
            issues.append("能量不足")
            recommendations.append("需要充足休息")
        
        # 检查快乐水平
        if self.happiness_level < 50:
            issues.append("快乐度偏低")
            recommendations.append("增加互动和运动")
        
        # 检查喂食情况
        if self.last_fed:
            hours_since_fed = (datetime.datetime.now() - self.last_fed).total_seconds() / 3600
            if hours_since_fed > 24:
                issues.append("长时间未进食")
                recommendations.append("立即提供食物")
        
        # 检查运动情况
        if self.last_exercise:
            days_since_exercise = (datetime.datetime.now() - self.last_exercise).days
            if days_since_exercise > 3:
                issues.append("缺乏运动")
                recommendations.append("安排适当的运动活动")
        
        wellness_score = max(0, 100 - len(issues) * 15 - (100 - self.happiness_level) * 0.3)
        
        return {
            'wellness_score': round(wellness_score, 1),
            'issues': issues,
            'recommendations': recommendations,
            'overall_status': 'excellent' if wellness_score >= 90 else 
                            'good' if wellness_score >= 70 else 
                            'fair' if wellness_score >= 50 else 'poor'
        }
    
    @classmethod
    def get_species_statistics(cls) -> Dict[str, Any]:
        """获取物种统计信息"""
        return {
            'total_animals': cls.total_animals,
            'species_breakdown': cls.species_registry.copy(),
            'most_common_species': max(cls.species_registry.items(), key=lambda x: x[1])[0] if cls.species_registry else None
        }
    
    def __str__(self) -> str:
        return f"{self.species} - {self.name} (ID: {self.animal_id})"
    
    def __repr__(self) -> str:
        return f"Animal(name='{self.name}', species='{self.species}', age={self.age})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Animal):
            return False
        return self.animal_id == other.animal_id
    
    def __hash__(self) -> int:
        return hash(self.animal_id)


# 工具函数
def create_animal_from_dict(data: Dict[str, Any]) -> Animal:
    """从字典数据创建动物对象"""
    # 这是一个工厂函数，实际使用时需要根据species创建具体的子类实例
    pass


def batch_animal_health_check(animals: List[Animal]) -> List[Dict[str, Any]]:
    """批量检查动物健康状况"""
    results = []
    for animal in animals:
        if animal.is_alive:
            wellness = animal.check_wellness()
            results.append({
                'animal': animal.get_basic_info(),
                'wellness': wellness
            })
    return results


def generate_feeding_schedule(animals: List[Animal]) -> Dict[str, List[Dict[str, Any]]]:
    """生成喂食计划"""
    schedule = {}
    for animal in animals:
        if animal.is_alive:
            needs = animal.calculate_daily_needs()
            schedule[animal.animal_id] = [
                {'time': '08:00', 'food_kg': needs['food_kg'] * 0.4, 'type': '早餐'},
                {'time': '18:00', 'food_kg': needs['food_kg'] * 0.6, 'type': '晚餐'}
            ]
    return schedule