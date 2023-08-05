#ifndef SETS_H
#define SETS_H

#include "Definitions.cpp"
#include "Sources.cpp"
#include "Sphere.cpp"
#include "Cylinder.cpp"
#include "CoreShell.cpp"
#include "Detectors.cpp"

namespace SPHERE
{
  class Set
  {
    public:
      DVector diameter;
      CVector index;
      std::vector<CVector> material;
      DVector n_medium;
      bool bounded_index;
      std::vector<State> States;

      Set(){}
      Set(DVector &diameter, std::vector<std::vector<complex128>> &material, DVector &n_medium)
          : diameter(diameter), material(material), n_medium(n_medium)
          {
            bounded_index=true;
          }

      Set(DVector &diameter, std::vector<complex128> &index, DVector &n_medium)
          : diameter(diameter), index(index), n_medium(n_medium)
          {
            bounded_index=false;
          }

      State operator[](size_t idx){return this->States[idx];}

   };
}


namespace CYLINDER
{
  class Set
  {
    public:
      DVector diameter;
      std::vector<complex128> index;
      std::vector<std::vector<complex128>> material;
      DVector n_medium;
      bool bounded_index;
      std::vector<State> States;

      Set(){}
      Set(DVector &diameter, std::vector<std::vector<complex128>> &material, DVector &n_medium)
          : diameter(diameter), material(material), n_medium(n_medium){bounded_index=true;}

      Set(DVector &diameter, std::vector<complex128> &index, DVector &n_medium)
          : diameter(diameter), index(index), n_medium(n_medium){bounded_index=false;}

      State operator[](size_t idx){return this->States[idx];}

  };
}


namespace CORESHELL
{
  class Set
  {
    public:
      DVector core_diameter, shell_diameter;
      std::vector<complex128> core_index, shell_index;
      std::vector<CVector> core_material, shell_material;
      DVector n_medium;
      bool bounded_core, bounded_shell;
      std::vector<State> States;

      Set(){}

      Set(DVector &core_diameter, DVector &shell_diameter, CVector &core_index, CVector &shell_index, DVector &n_medium)
      : core_diameter(core_diameter), shell_diameter(shell_diameter), core_index(core_index), shell_index(shell_index), n_medium(n_medium)
        { bounded_core=false; bounded_shell=false; }

      Set(DVector &core_diameter, DVector &shell_diameter, CVector &core_index, std::vector<CVector> &shell_material, DVector &n_medium)
      : core_diameter(core_diameter), shell_diameter(shell_diameter), core_index(core_index), shell_material(shell_material), n_medium(n_medium)
        { bounded_core=false; bounded_shell=true; }

      Set(DVector &core_diameter, DVector &shell_diameter, std::vector<CVector> &core_material, CVector &shell_index, DVector &n_medium)
      : core_diameter(core_diameter), shell_diameter(shell_diameter), core_material(core_material), shell_index(shell_index), n_medium(n_medium)
        {bounded_core=true; bounded_shell=false;}

      Set(DVector &core_diameter, DVector &shell_diameter, std::vector<CVector> &core_material, std::vector<CVector> &shell_material, DVector &n_medium)
      : core_diameter(core_diameter), shell_diameter(shell_diameter), core_material(core_material), shell_material(shell_material), n_medium(n_medium)
        {bounded_core=true; bounded_shell=true;}

        State operator[](size_t idx){return this->States[idx];}
  };
}





namespace SOURCE
{
    class Set
    {
      public:
        DVector wavelength;
        std::vector<CVector> jones_vector;
        DVector amplitude;
        std::vector<State> States;

        Set(){}
        Set(DVector &wavelength, std::vector<CVector> &jones_vector, DVector &amplitude)
        : wavelength(wavelength), jones_vector(jones_vector), amplitude(amplitude)
        {}

        State operator[](size_t idx){return this->States[idx];}

    };
}

namespace DETECTOR
{
  class Set
  {
    public:
      std::vector<CVector> ScalarField;
      DVector NA, PhiOffset, GammaOffset, Filter;
      bool Coherent, PointCoupling;
      std::vector<State> States;

      Set(){}
      Set(std::vector<CVector> &ScalarField,
          DVector &NA,
          DVector &PhiOffset,
          DVector &GammaOffset,
          DVector &Filter,
          bool    &Coherent,
          bool    &PointCoupling)
      : ScalarField(ScalarField),
        NA(NA),
        PhiOffset(PhiOffset),
        GammaOffset(GammaOffset),
        Filter(Filter),
        Coherent(Coherent),
        PointCoupling(PointCoupling)
      {}

      State operator[](size_t idx){return this->States[idx];}

  };

}


#endif
