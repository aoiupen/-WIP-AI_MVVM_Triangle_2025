"""
어댑터 패턴 간단 테스트

이 스크립트는 ML 모델 어댑터 패턴의 구현을 빠르게 테스트합니다.
"""

import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 경로 디버깅 (선택사항)
print(f"현재 디렉토리: {os.getcwd()}")
print(f"Python 경로: {sys.path[0]}")

from models.triangle_model import TriangleModel

def main():
    # 모델 인스턴스 생성
    try:
        print("1. 모델 로드 테스트 시작...")
        model = TriangleModel(model_path=None)
        print("✓ 모델 로드 성공\n")
        
        print("2. 어댑터 정보 확인...")
        adapter_name = model.adapter.get_framework_name()
        print(f"✓ 사용 중인 어댑터: {adapter_name}\n")
        
        print("3. 유효한 삼각형 테스트...")
        valid_triangle = [3, 4, 5]
        valid_result = model.predict(valid_triangle)
        print(f"✓ 유효한 삼각형 {valid_triangle}: {valid_result:.4f}")
        if valid_result > 0.5:
            print("  결과 해석: 삼각형이 유효함 (예상대로)\n")
        else:
            print("  결과 해석: 삼각형이 유효하지 않음 (예상과 다름!)\n")
        
        print("4. 유효하지 않은 삼각형 테스트...")
        invalid_triangle = [1, 2, 10]
        invalid_result = model.predict(invalid_triangle)
        print(f"✓ 유효하지 않은 삼각형 {invalid_triangle}: {invalid_result:.4f}")
        if invalid_result < 0.5:
            print("  결과 해석: 삼각형이 유효하지 않음 (예상대로)\n")
        else:
            print("  결과 해석: 삼각형이 유효함 (예상과 다름!)\n")
        
        print("모든 테스트 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()