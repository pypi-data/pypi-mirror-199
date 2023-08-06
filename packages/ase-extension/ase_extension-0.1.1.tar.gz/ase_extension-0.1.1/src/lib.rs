pub mod logfermi;
pub mod rmsd;

use crate::rmsd::compute_minimum_rmsd;
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray2};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

#[pymodule]
fn ase_extension(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn log_fermi<'py>(
        _py: Python<'py>,
        positions: PyReadonlyArray2<f64>,
        radius: f64,
        temperature: f64,
        beta: f64,
    ) -> (f64, &'py PyArray2<f64>) {
        let positions = positions.as_array();
        let (e, e_grad) = logfermi::log_fermi(&positions, radius, temperature, beta);
        (e, e_grad.into_pyarray(_py))
    }

    #[pyfn(m)]
    fn rmsd<'py>(
        _py: Python<'py>,
        positions_1: PyReadonlyArray2<f64>,
        positions_2: PyReadonlyArray2<f64>,
        compute_gradient: bool,
    ) -> (
        f64,
        Option<&'py PyArray2<f64>>,
        &'py PyArray2<f64>,
        &'py PyArray1<f64>,
    ) {
        let positions_1 = positions_1.as_array();
        let positions_2 = positions_2.as_array();
        let result = compute_minimum_rmsd(&positions_1, &positions_2, compute_gradient);
        let rmsd_grad = result.rmsd_grad.map(|x| x.into_pyarray(_py));
        (
            result.rmsd_val,
            rmsd_grad,
            result.rotation_matrix.into_pyarray(_py),
            result.translation_vector.into_pyarray(_py),
        )
    }

    Ok(())
}
