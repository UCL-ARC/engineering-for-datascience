identifiers {
  type: REACTION_CXSMILES
  value: "[CH3:1][O:2][C:3]1[CH:8]=[C:7]([O:9][CH3:10])[CH:6]=[CH:5][C:4]=1[C:11]1[NH:12][C:13]2[C:14]([N:20]=1)=[N+:15]([O-])[CH:16]=[CH:17][CH:18]=2.Cl.[OH2:22]>C(OC(=O)C)(=O)C>[CH3:1][O:2][C:3]1[CH:8]=[C:7]([O:9][CH3:10])[CH:6]=[CH:5][C:4]=1[C:11]1[N:20]=[C:14]2[NH:15][C:16](=[O:22])[CH2:17][CH:18]=[C:13]2[N:12]=1"
  is_mapped: true
}
inputs {
  key: "m1"
  value {
    components {
      identifiers {
        type: NAME
        value: "2-(2,4-dimethoxy-phenyl)-imidazo[4,5-b]pyridin-4-oxide"
      }
      identifiers {
        type: SMILES
        value: "COC1=C(C=CC(=C1)OC)C=1NC=2C(=[N+](C=CC2)[O-])N1"
      }
      identifiers {
        type: INCHI
        value: "InChI=1S/C14H13N3O3/c1-19-9-5-6-10(12(8-9)20-2)13-15-11-4-3-7-17(18)14(11)16-13/h3-8H,1-2H3,(H,15,16)"
      }
      amount {
        moles {
          value: 0.0
          precision: 1.0
          units: MOLE
        }
      }
      reaction_role: REACTANT
    }
  }
}
inputs {
  key: "m2_m3"
  value {
    components {
      identifiers {
        type: NAME
        value: "ice"
      }
      amount {
        volume {
          value: 150.0
          units: MILLILITER
        }
      }
      reaction_role: REACTANT
    }
    components {
      identifiers {
        type: NAME
        value: "hydrochloric acid"
      }
      identifiers {
        type: SMILES
        value: "Cl"
      }
      identifiers {
        type: INCHI
        value: "InChI=1S/ClH/h1H"
      }
      amount {
        volume {
          value: 25.0
          units: MILLILITER
        }
      }
      reaction_role: REACTANT
    }
  }
}
inputs {
  key: "m4"
  value {
    components {
      identifiers {
        type: NAME
        value: "water"
      }
      identifiers {
        type: SMILES
        value: "O"
      }
      identifiers {
        type: INCHI
        value: "InChI=1S/H2O/h1H2"
      }
      amount {
        volume {
          value: 50.0
          units: MILLILITER
        }
      }
      reaction_role: REACTANT
    }
  }
}
inputs {
  key: "m5"
  value {
    components {
      identifiers {
        type: NAME
        value: "acetic anhydride"
      }
      identifiers {
        type: SMILES
        value: "C(C)(=O)OC(C)=O"
      }
      identifiers {
        type: INCHI
        value: "InChI=1S/C4H6O3/c1-3(5)7-4(2)6/h1-2H3"
      }
      amount {
        volume {
          value: 40.0
          units: MILLILITER
        }
      }
      reaction_role: SOLVENT
    }
  }
}
conditions {
  temperature {
    setpoint {
      value: 120.0
      units: CELSIUS
    }
  }
  stirring {
    type: CUSTOM
    details: "the mixture is stirred at 120\302\260 C. for 30 minutes"
  }
  conditions_are_dynamic: true
  details: "See reaction.notes.procedure_details."
}
notes {
  procedure_details: "Four grams of 2-(2,4-dimethoxy-phenyl)-imidazo[4,5-b]pyridin-4-oxide is suspended in 40 ml of acetic anhydride and refluxed for 2.75 hours. After cooling the mixture is poured onto 150 ml of ice, 25 ml of 6N hydrochloric acid are added, and the mixture is stirred at 120\302\260 C. for 30 minutes. It is cooled to ambient temperature, 50 ml of water are added, and the precipitate is subjected to suction filtration. The product is purified by chromatography on silica gel [eluant: methylene chloride/methanol (100:0 to 100:10)]."
}
workups {
  type: TEMPERATURE
  details: "refluxed for 2.75 hours"
  duration {
    value: 2.75
    units: HOUR
  }
}
workups {
  type: TEMPERATURE
  details: "After cooling the mixture"
}
workups {
  type: ADDITION
  details: "are added"
}
workups {
  type: TEMPERATURE
  details: "It is cooled to ambient temperature"
  temperature {
    control {
      type: AMBIENT
    }
  }
}
workups {
  type: FILTRATION
  details: "the precipitate is subjected to suction filtration"
}
workups {
  type: CUSTOM
  details: "The product is purified by chromatography on silica gel [eluant: methylene chloride/methanol (100:0 to 100:10)]"
  input {
    components {
      identifiers {
        type: NAME
        value: "methylene chloride methanol"
      }
      identifiers {
        type: SMILES
        value: "C(Cl)Cl.CO"
      }
      identifiers {
        type: INCHI
        value: "InChI=1S/CH2Cl2.CH4O/c2-1-3;1-2/h1H2;2H,1H3"
      }
      amount {
        moles {
          value: 0.0
          precision: 1.0
          units: MOLE
        }
      }
      reaction_role: WORKUP
    }
  }
}
outcomes {
  reaction_time {
    value: 30.0
    units: MINUTE
  }
  products {
    identifiers {
      type: NAME
      value: "2-(2,4-Dimethoxy-phenyl)-4H-imidazo[4,5-b]pyridin-5-one"
    }
    identifiers {
      type: SMILES
      value: "COC1=C(C=CC(=C1)OC)C1=NC=2C(NC(CC2)=O)=N1"
    }
    identifiers {
      type: INCHI
      value: "InChI=1S/C14H13N3O3/c1-19-8-3-4-9(11(7-8)20-2)13-15-10-5-6-12(18)16-14(10)17-13/h3-5,7H,6H2,1-2H3,(H,15,16,17,18)"
    }
  }
}
provenance {
  doi: "10.6084/m9.figshare.5104873.v1"
  patent: "US04722929"
  record_created {
    time {
      value: "2022-12-02 17:04:29.167310"
    }
    person {
      username: "skearnes"
      name: "Steven Kearnes"
      orcid: "0000-0003-4579-4388"
      organization: "Google LLC"
      email: "kearnes@google.com"
    }
  }
  record_modified {
    time {
      value: "Mon Dec  5 19:48:40 2022"
    }
    person {
      username: "github-actions"
      email: "github-actions@github.com"
    }
    details: "Automatic updates from the submission pipeline."
  }
}
reaction_id: "ord-eed20875f89042a78eaca70db7681c77"
