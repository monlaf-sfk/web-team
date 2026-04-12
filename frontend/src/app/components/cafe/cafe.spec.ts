import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Cafe } from './cafe';

describe('Cafe', () => {
  let component: Cafe;
  let fixture: ComponentFixture<Cafe>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Cafe],
    }).compileComponents();

    fixture = TestBed.createComponent(Cafe);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
