# cranial-superimposition
### Updated on 2025 August 12:
#### 3D Skull and Face Geometric Feature Mapping

1. **Overview**: Extract depth, curvature, and elevation features from 3D models and project them to 2D feature maps for model training.
2. **Formulas**
   - **Depth**: $a_{i}=-z_{i} × \frac{m}{2}+\frac{n}{2}, b_{i}=x_{i} × \frac{m}{2}+\frac{n}{2}, D(a_{i}, b_{i})=y_{i}$
   - **Curvature**: $E_{i}(B)=\frac{1}{|B|} \sum_{e \in B} \beta(e)\| e \cap B\| \overline{e}^{T} \cdot \overline{e}, \beta(e)=\cos ^{-1}\left(\frac{\vec{n}_{1} \cdot \vec{n}_{2}}{\left|\vec{n}_{1}\right|\left|\vec{n}_{2}\right|}\right)$
   - **Elevation**: $r = \sqrt{x^{2}+y^{2}+z^{2}}, \begin{cases}x=r \cdot \sin (\phi) \cdot \cos (\theta)\\y=r \cdot \sin (\phi) \cdot \sin (\theta)\\z=r \cdot \cos (\phi)\end{cases}$
3. **Process**: Read 3D data, calculate features, and arrange them into 2D maps.

#### Metric Learning using Triplet Network

1. **Overview**: Use a triplet network for skull - face matching. Incorporate triplet and Sinkhorn losses to learn discriminative embeddings and improve accuracy.
2. **Formulas**
   - **Triplet Loss**: $L_{Triplet }=\max \left(\left\| S_{a}-F_{p}\right\| ^{2}-\left\| F_{a}-F_{n}\right\| ^{2}+margin, 0\right)$
   - **Sinkhorn Distance**: $W_{\epsilon}(S, F)=\min _{\pi \in \Pi(S, F)} \sum_{i=1}^{n} \sum_{j=1}^{m} \pi_{i j} M_{i j}+\epsilon H(\pi)$
   - **Sinkhorn Loss**: $L_{Sinkhorn }=\max \left(\frac{W_{p}-W_{n}}{W_{p}+W_{n}+\delta}+margin, 0\right)$
3. **Process**: Build a triplet network, extract features, calculate losses, and optimize parameters through back - propagation. 



### Updated on 2025 August 06:
The conference is underway, and our relevant code will be ready for release after the official presentation of the paper.

### Updated on December 21:
The 2025 IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP) has accepted the paper. After the paper's official acceptance, the code (including feature map mapping and network training), pre-trained weights, and data preprocessing pipeline will be released.

The code used for cranial superimposition is available here. After our paper is officially published, the trained weights and detailed implementation will be provided.
![Description of the image](./Img00.png)
