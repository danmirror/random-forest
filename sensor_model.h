#ifndef SENSOR_MODEL_H
#define SENSOR_MODEL_H

// Random Forest with 5 trees

int predict_tree_0(float temperature, int gsr, int bpm) {
    if (temperature <= 36.53) {
        if (gsr <= 4.73) {
            if (bpm <= 63.00) {
                return 2;
            }
            if (bpm > 63.00) {
                if (bpm <= 71.00) {
                    if (bpm <= 69.50) {
                        return 1;
                    }
                    if (bpm > 69.50) {
                        return 1;
                    }
                }
                if (bpm > 71.00) {
                    return 1;
                }
            }
        }
        if (gsr > 4.73) {
            return 0;
        }
    }
    if (temperature > 36.53) {
        if (temperature <= 37.53) {
            if (temperature <= 37.32) {
                if (temperature <= 37.31) {
                    if (bpm <= 75.00) {
                        return 2;
                    }
                    if (bpm > 75.00) {
                        return 3;
                    }
                }
                if (temperature > 37.31) {
                    return 3;
                }
            }
            if (temperature > 37.32) {
                return 2;
            }
        }
        if (temperature > 37.53) {
            return 3;
        }
    }
}

int predict_tree_1(float temperature, int gsr, int bpm) {
    if (bpm <= 79.00) {
        if (bpm <= 65.50) {
            if (bpm <= 64.50) {
                return 2;
            }
            if (bpm > 64.50) {
                if (gsr <= 3.69) {
                    return 1;
                }
                if (gsr > 3.69) {
                    return 2;
                }
            }
        }
        if (bpm > 65.50) {
            if (bpm <= 74.50) {
                if (temperature <= 36.53) {
                    if (temperature <= 35.34) {
                        return 0;
                    }
                    if (temperature > 35.34) {
                        return 1;
                    }
                }
                if (temperature > 36.53) {
                    return 2;
                }
            }
            if (bpm > 74.50) {
                if (temperature <= 35.90) {
                    return 0;
                }
                if (temperature > 35.90) {
                    if (gsr <= 4.98) {
                        return 1;
                    }
                    if (gsr > 4.98) {
                        return 0;
                    }
                }
            }
        }
    }
    if (bpm > 79.00) {
        return 3;
    }
}

int predict_tree_2(float temperature, int gsr, int bpm) {
    if (gsr <= 4.48) {
        if (gsr <= 4.32) {
            if (gsr <= 3.99) {
                if (temperature <= 36.07) {
                    return 1;
                }
                if (temperature > 36.07) {
                    if (bpm <= 67.50) {
                        return 2;
                    }
                    if (bpm > 67.50) {
                        return 1;
                    }
                }
            }
            if (gsr > 3.99) {
                if (bpm <= 65.00) {
                    return 2;
                }
                if (bpm > 65.00) {
                    if (bpm <= 68.00) {
                        return 1;
                    }
                    if (bpm > 68.00) {
                        return 1;
                    }
                }
            }
        }
        if (gsr > 4.32) {
            if (gsr <= 4.33) {
                return 2;
            }
            if (gsr > 4.33) {
                return 1;
            }
        }
    }
    if (gsr > 4.48) {
        if (temperature <= 36.23) {
            return 0;
        }
        if (temperature > 36.23) {
            return 3;
        }
    }
}

int predict_tree_3(float temperature, int gsr, int bpm) {
    if (bpm <= 75.50) {
        if (gsr <= 4.78) {
            if (temperature <= 36.07) {
                if (temperature <= 35.95) {
                    return 1;
                }
                if (temperature > 35.95) {
                    if (gsr <= 4.15) {
                        return 1;
                    }
                    if (gsr > 4.15) {
                        return 2;
                    }
                }
            }
            if (temperature > 36.07) {
                if (temperature <= 36.53) {
                    if (gsr <= 3.31) {
                        return 1;
                    }
                    if (gsr > 3.31) {
                        return 2;
                    }
                }
                if (temperature > 36.53) {
                    return 2;
                }
            }
        }
        if (gsr > 4.78) {
            return 0;
        }
    }
    if (bpm > 75.50) {
        if (bpm <= 79.00) {
            return 0;
        }
        if (bpm > 79.00) {
            if (temperature <= 35.85) {
                return 0;
            }
            if (temperature > 35.85) {
                return 3;
            }
        }
    }
}

int predict_tree_4(float temperature, int gsr, int bpm) {
    if (bpm <= 79.00) {
        if (gsr <= 4.78) {
            if (temperature <= 36.06) {
                if (temperature <= 35.95) {
                    return 1;
                }
                if (temperature > 35.95) {
                    if (temperature <= 36.02) {
                        return 1;
                    }
                    if (temperature > 36.02) {
                        return 1;
                    }
                }
            }
            if (temperature > 36.06) {
                if (temperature <= 36.52) {
                    if (bpm <= 70.50) {
                        return 2;
                    }
                    if (bpm > 70.50) {
                        return 1;
                    }
                }
                if (temperature > 36.52) {
                    return 2;
                }
            }
        }
        if (gsr > 4.78) {
            return 0;
        }
    }
    if (bpm > 79.00) {
        if (bpm <= 83.50) {
            if (bpm <= 81.50) {
                return 3;
            }
            if (bpm > 81.50) {
                if (temperature <= 36.57) {
                    return 0;
                }
                if (temperature > 36.57) {
                    return 3;
                }
            }
        }
        if (bpm > 83.50) {
            return 3;
        }
    }
}

String predictSensorCondition(float temperature, int gsr, int bpm) {
    int votes[5];
    votes[0] = predict_tree_0(temperature, gsr, bpm);
    votes[1] = predict_tree_1(temperature, gsr, bpm);
    votes[2] = predict_tree_2(temperature, gsr, bpm);
    votes[3] = predict_tree_3(temperature, gsr, bpm);
    votes[4] = predict_tree_4(temperature, gsr, bpm);
    int count[10] = {0};
    for (int i = 0; i < 5; i++) count[votes[i]]++;
    int max_idx = 0;
    for (int i = 1; i < 10; i++) {
        if (count[i] > count[max_idx]) max_idx = i;
    }
    switch (max_idx) {
        case 0: return "Anxious";
        case 1: return "Calm";
        case 2: return "Relax";
        case 3: return "Stress";
        default: return "unknown";
    }
}

#endif