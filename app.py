import streamlit as st
import pyvista as pv
from st_pyvista import st_pyvista
import tempfile
import os

# Streamlit 페이지 설정
st.set_page_config(layout="wide") # 페이지 레이아웃을 넓게 설정
st.title("STEP 파일 3D 뷰어 (GeoHealer AI 데모)")
st.write("STEP 또는 STL 파일을 업로드하여 3D 모델을 웹에서 확인하세요.")

# 파일 업로더 위젯
uploaded_file = st.file_uploader("STEP 또는 STL 파일 업로드", type=["step", "stl", "stp"])

if uploaded_file is not None:
    # 1. 임시 파일로 저장
    # Streamlit은 업로드된 파일을 직접 PyVista로 전달하기 어려우므로, 임시 파일로 저장
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        try:
            # 2. PyVista로 파일 로드
            # PyVista는 STEP, STL 등 다양한 3D 형식을 지원합니다.
            mesh = pv.read(file_path)

            # 3. PyVista 플로터 생성 및 메쉬 추가
            plotter = pv.Plotter(window_size=[800, 600]) # 뷰어 크기 설정
            plotter.add_mesh(mesh, color="lightblue", show_edges=True) # 모델 추가, 색상, 엣지 표시
            plotter.show_axes() # 축 표시

            st.subheader("업로드된 3D 모델:")
            # 4. st_pyvista를 사용하여 Streamlit에 3D 뷰어 임베딩
            st_pyvista(plotter, key="3d_viewer") # key는 Streamlit 위젯의 고유 ID

            st.success("모델 로드 및 렌더링 성공!")
            st.write(f"파일 이름: {uploaded_file.name}")
            st.write(f"메쉬 정보: {mesh.n_points} 점, {mesh.n_cells} 셀")

        except Exception as e:
            st.error(f"파일 로드 또는 렌더링 중 오류 발생: {e}")
            st.info("지원되지 않는 형식 또는 파일 손상 여부를 확인해주세요.")

else:
    st.info("STEP 또는 STL 파일을 업로드하여 3D 모델을 확인해 보세요.")

st.sidebar.markdown("---")
st.sidebar.markdown("### GeoHealer AI 데모")
st.sidebar.markdown("이 페이지는 GDL 기반 결함 자동 보정 솔루션의 시각화 데모입니다.")