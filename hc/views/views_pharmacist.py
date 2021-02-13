from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Patient
from hc.forms.forms_pharmacist import ViewPrescriptionForm
from hc.forms.forms_doctor import SearchPatientForm


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='pharmacist').exists())
def IndexViewPharmacist(request):
    form = SearchPatientForm()
    if request.method == "POST":
        username = request.POST.get('username', False)
        return redirect('hc:view_prescription', username=username)
    else:
        return render(request, 'pharmacist/index.html', {'form': form})


@login_required(login_url="/accounts/login/")
@user_passes_test(lambda u: u.groups.filter(name='pharmacist').exists())
def ViewPrescription(request, username):
    patient = Patient.objects.filter(user__username=username)[0]
    pres = patient.prescriptions.filter(utilised=False).latest('created_at')
    pres.remarks = pres.ENCRYPTER.decrypt(pres.remarks.encode('utf-8')).decode('utf-8')
    if request.method == "POST":
        form = ViewPrescriptionForm(request.POST, instance=pres)
        form.save()
        return redirect('main:home')
    form = ViewPrescriptionForm(instance=pres)
    return render(request, 'pharmacist/prescription.html', {'form': form})
