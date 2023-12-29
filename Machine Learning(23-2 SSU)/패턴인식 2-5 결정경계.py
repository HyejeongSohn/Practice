import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# 정규분포 함수를 위한 평균과 공분산 행렬 정의
mean1 = [3, 2]
cov1 = [[3, 1], [1, 2]]
mean2 = [-3, 4]
cov2 = [[3, 1], [1, 2]]

# 정규분포 객체 생성
rv1 = multivariate_normal(mean1, cov1)
rv2 = multivariate_normal(mean2, cov2)

# x와 y 범위 설정
x = np.linspace(-10, 10, 500)
y = np.linspace(-10, 10, 500)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

# 정규분포 함수 값 계산
Z1 = rv1.pdf(pos)
Z2 = rv2.pdf(pos)

# 등고선 그래프 그리기
plt.contour(X, Y, Z1, colors='b', levels=5)
plt.contour(X, Y, Z2, colors='r', levels=5)

# 결정 경계 그래프 추가
# 여기서는 간단하게 두 클래스의 정규분포 함수 값이 동일한 지점을 결정 경계로 설정
plt.contour(X, Y, Z1 - Z2, levels=[0], colors='k')

# 그래프 레이블과 제목 추가
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('결정 경계')

# 그래프 표시
plt.show()