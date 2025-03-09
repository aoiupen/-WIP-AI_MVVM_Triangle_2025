class TriangleModel:
    """삼각형을 표현하는 도메인 모델 클래스"""
    
    def __init__(self, validator):
        """
        삼각형 모델 초기화
        
        Args:
            validator: TriangleValidatorCore 인스턴스
        """
        self.validator = validator
        self.sides = [0, 0, 0]
        self.math_result = False
        self.ai_prediction_value = 0.0
        self.is_valid_by_ai = False
        self.is_consistent = False
    
    def validate(self, a, b, c):
        """
        세 변의 길이로 삼각형을 검증합니다.
        
        Args:
            a, b, c: 삼각형의 세 변 길이
            
        Returns:
            검증 결과를 담은 딕셔너리
        """
        # 입력값 정규화 (오름차순 정렬)
        self.sides = sorted([float(a), float(b), float(c)])
        
        # 검증 수행
        result = self.validator.validate(*self.sides)
        
        # 결과 저장
        self.math_result = result["math_result"]
        self.ai_prediction_value = result["ai_prediction_value"]
        self.is_valid_by_ai = result["is_valid_by_ai"]
        self.is_consistent = result["is_consistent"]
        
        return result