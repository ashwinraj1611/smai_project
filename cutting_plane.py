import numpy as numpy
def cutting_plane (U,I,y_u,y,W,C,th):
	U=np.array(U)
	I=np.array(I)
	y_u=np.array(y_u)

	UT=np.transpose(U)

	Hu=[]

	count=0;

	for i in UT:

		z1=0

		for j in y:
			for k in y_u:
				z1=z1+np.tanspose(i)*(j-k)

		z2=0

		for j in y:
			for k in y:
				if(j!=k):
					z2=z2+(np.dot(j,k)/(len(j)*len(k)))

		z3= 0

		for j in y:
			temp=0
			for k in j:
				temp+=k**2
			z3=z3+temp**0.5

		z4=0



		for j in y:
			z4+=j

		zu= np.linalg.norm(u)


		JFM=[z1,z2,zu,z3,u,z4]


		H=(y_u-y)+np.tanspose(W)*JFM;

		Hu.append(H)

		y_bar= max(Hu)



	kai=max(0,sum(Hu)/len(Hu))

	if(sum(Hu)/len(Hu)) > kai + th:
		W.append(y_bar)

	return W